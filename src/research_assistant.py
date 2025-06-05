#!/usr/bin/env python3

import argparse
import json
from datetime import datetime
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import pandas as pd
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ResearchAssistant:
    def __init__(self):
        """Initialize the Research Assistant with necessary models and configurations."""
        logger.info("Initializing Research Assistant...")
        try:
            # Initialize the summarization and sentiment analysis pipelines
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
            logger.info("Models loaded successfully")
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
            raise
        
    def scrape_news(self, topic: str, num_articles: int = 5) -> List[Dict]:
        """
        Scrape news articles related to the given topic using NewsAPI
        
        Args:
            topic (str): The topic to search for
            num_articles (int): Number of articles to fetch
            
        Returns:
            List[Dict]: List of processed articles with their content
        """
        # TODO: Replace with your NewsAPI key
        API_KEY = "YOUR_NEWS_API_KEY"
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={API_KEY}&language=en&sortBy=publishedAt"
        
        try:
            logger.info(f"Fetching news articles for topic: {topic}")
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json()["articles"][:num_articles]
            
            processed_articles = []
            for article in articles:
                logger.info(f"Processing article: {article['title']}")
                processed_articles.append({
                    "title": article["title"],
                    "url": article["url"],
                    "published_at": article["publishedAt"],
                    "content": self._extract_article_content(article["url"])
                })
            return processed_articles
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []

    def _extract_article_content(self, url: str) -> str:
        """
        Extract the main content from a news article URL
        
        Args:
            url (str): URL of the article to extract content from
            
        Returns:
            str: Extracted and cleaned content
        """
        try:
            logger.info(f"Extracting content from: {url}")
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            # Get the main content (this is a simple approach, might need refinement)
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs])
            return content[:1000]  # Limit content length
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return ""

    def summarize_article(self, content: str) -> str:
        """
        Generate a summary of the article content
        
        Args:
            content (str): Article content to summarize
            
        Returns:
            str: Generated summary
        """
        try:
            logger.info("Generating summary...")
            summary = self.summarizer(content, max_length=130, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            logger.error(f"Error summarizing content: {e}")
            return ""

    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze the sentiment of the given text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Sentiment analysis results
        """
        try:
            logger.info("Analyzing sentiment...")
            result = self.sentiment_analyzer(text)[0]
            return {
                "sentiment": result["label"],
                "score": result["score"]
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"sentiment": "ERROR", "score": 0.0}

    def generate_report(self, topic: str, articles: List[Dict]) -> Dict:
        """
        Generate a comprehensive report from the analyzed articles
        
        Args:
            topic (str): Research topic
            articles (List[Dict]): List of processed articles
            
        Returns:
            Dict: Generated report
        """
        logger.info(f"Generating report for topic: {topic}")
        report = {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "articles": []
        }

        for article in articles:
            summary = self.summarize_article(article["content"])
            sentiment = self.analyze_sentiment(article["content"])
            
            report["articles"].append({
                "title": article["title"],
                "url": article["url"],
                "published_at": article["published_at"],
                "summary": summary,
                "sentiment": sentiment
            })

        return report

    def save_report(self, report: Dict, output_dir: str = "reports"):
        """
        Save the report to a JSON file
        
        Args:
            report (Dict): Report to save
            output_dir (str): Directory to save the report in
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = output_path / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Report saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving report: {e}")

def main():
    parser = argparse.ArgumentParser(description="Research Assistant for News Analysis")
    parser.add_argument("topic", help="Topic to research")
    parser.add_argument("--num-articles", type=int, default=5, help="Number of articles to analyze")
    parser.add_argument("--output-dir", type=str, default="reports", help="Directory to save reports")
    args = parser.parse_args()

    try:
        assistant = ResearchAssistant()
        articles = assistant.scrape_news(args.topic, args.num_articles)
        
        if articles:
            report = assistant.generate_report(args.topic, articles)
            assistant.save_report(report, args.output_dir)
        else:
            logger.warning("No articles found for the given topic.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 