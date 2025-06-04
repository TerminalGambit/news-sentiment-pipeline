"""
Sentiment analysis module using FinBERT model.
"""

import logging
from typing import Any, Dict, List

import torch
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from .config import MODEL_NAME, SENTIMENT_LABELS

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Class for performing sentiment analysis using FinBERT."""

    def __init__(self):
        """Initialize the sentiment analyzer with FinBERT model."""
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info("Using device: %s", self.device)

            # Load model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

            # Create pipeline
            self.analyzer = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
            )

            logger.info("Successfully initialized sentiment analyzer")

        except Exception as e:
            logger.error("Error initializing sentiment analyzer: %s", str(e))
            raise

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a single text.

        Args:
            text (str): Input text

        Returns:
            Dict[str, Any]: Sentiment analysis results
        """
        try:
            result = self.analyzer(text)[0]
            return {
                "label": SENTIMENT_LABELS.get(result["label"].lower(), result["label"]),
                "score": round(result["score"], 3),
            }
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error analyzing text: %s", str(e))
            return {"label": "Unknown", "score": 0.0}

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment of multiple texts.

        Args:
            texts (List[str]): List of input texts

        Returns:
            List[Dict[str, Any]]: List of sentiment analysis results
        """
        results = []
        for text in tqdm(texts, desc="Analyzing sentiments"):
            result = self.analyze_text(text)
            results.append(result)
        return results

    def analyze_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment of multiple articles.

        Args:
            articles (List[Dict[str, Any]]): List of articles

        Returns:
            List[Dict[str, Any]]: List of articles with sentiment analysis
        """
        processed_articles = []

        for article in tqdm(articles, desc="Processing articles"):
            if "processed_text" not in article:
                logger.warning("Article missing processed text, skipping")
                continue

            sentiment = self.analyze_text(article["processed_text"])
            article["sentiment"] = sentiment
            processed_articles.append(article)

        return processed_articles
