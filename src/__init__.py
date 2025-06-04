"""
Financial News Sentiment Analysis Package
"""

from .news_ingestion import fetch_all_feeds
from .pipeline import SentimentAnalysisPipeline
from .sentiment_analyzer import SentimentAnalyzer
from .storage import DataStorage
from .text_processor import process_article

__version__ = "1.0.0"
__all__ = [
    "SentimentAnalysisPipeline",
    "fetch_all_feeds",
    "process_article",
    "SentimentAnalyzer",
    "DataStorage",
]
