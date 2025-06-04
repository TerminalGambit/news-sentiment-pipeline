"""
Financial News Sentiment Analysis Package
"""

from .pipeline import SentimentAnalysisPipeline
from .news_ingestion import fetch_all_feeds
from .text_processor import process_article
from .sentiment_analyzer import SentimentAnalyzer
from .storage import DataStorage

__version__ = "1.0.0"
__all__ = [
    'SentimentAnalysisPipeline',
    'fetch_all_feeds',
    'process_article',
    'SentimentAnalyzer',
    'DataStorage'
] 