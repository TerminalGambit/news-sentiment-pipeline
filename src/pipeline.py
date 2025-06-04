"""
Main pipeline module for orchestrating the sentiment analysis process.
"""

import logging
from typing import List, Dict, Any
from datetime import datetime
import time

from .news_ingestion import fetch_all_feeds
from .text_processor import process_article
from .sentiment_analyzer import SentimentAnalyzer
from .storage import DataStorage
from .report_generator import ReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SentimentAnalysisPipeline:
    def __init__(self):
        """Initialize the pipeline components."""
        self.analyzer = SentimentAnalyzer()
        self.storage = DataStorage()
        self.report_generator = ReportGenerator()

    def run(self, save_csv: bool = True, generate_report: bool = True) -> List[Dict[str, Any]]:
        """
        Run the complete sentiment analysis pipeline.
        
        Args:
            save_csv (bool): Whether to save results in CSV format
            generate_report (bool): Whether to generate a LaTeX report
            
        Returns:
            List[Dict[str, Any]]: Processed articles with sentiment analysis
        """
        start_time = time.time()
        logger.info("Starting sentiment analysis pipeline")
        
        try:
            # 1. Fetch news articles
            logger.info("Fetching news articles...")
            articles = fetch_all_feeds()
            
            if not articles:
                logger.warning("No articles fetched, ending pipeline")
                return []
                
            # 2. Process articles
            logger.info("Processing articles...")
            processed_articles = []
            for article in articles:
                processed = process_article(article)
                if processed:
                    processed_articles.append(processed)
                    
            if not processed_articles:
                logger.warning("No articles processed successfully, ending pipeline")
                return []
                
            # 3. Analyze sentiment
            logger.info("Analyzing sentiment...")
            results = self.analyzer.analyze_articles(processed_articles)
            
            # 4. Save results
            logger.info("Saving results...")
            self.storage.save_to_json(results)
            
            if save_csv:
                self.storage.save_to_csv(results)
                
            # 5. Generate report if requested
            if generate_report:
                logger.info("Generating report...")
                report_path = self.report_generator.generate_report(results)
                logger.info(f"Report generated: {report_path}")
                
            # Log summary
            duration = time.time() - start_time
            logger.info(f"Pipeline completed in {duration:.2f} seconds")
            logger.info(f"Processed {len(results)} articles")
            
            # Log sentiment distribution
            sentiment_counts = {}
            for result in results:
                label = result['sentiment']['label']
                sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
                
            logger.info("Sentiment distribution:")
            for label, count in sentiment_counts.items():
                logger.info(f"{label}: {count} articles")
                
            return results
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            return []

def main():
    """Main entry point for the pipeline."""
    pipeline = SentimentAnalysisPipeline()
    pipeline.run()

if __name__ == "__main__":
    main() 