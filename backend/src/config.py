"""
Application configuration.
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directory
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Reports directory
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# API configuration
API_CONFIG = {
    "title": "Sentiment Analysis API",
    "version": "1.0.0",
    "description": "API for sentiment analysis and market data",
}

# Sentiment analysis configuration
SENTIMENT_CONFIG = {
    "model_name": "distilbert-base-uncased-finetuned-sst-2-english",
    "batch_size": 32,
    "max_length": 512,
}

# Market data configuration
MARKET_CONFIG = {
    "default_symbols": ["BTC-USD", "ETH-USD"],
    "default_timeframe": "1d",
    "default_period": "1y",
    "cache_duration": 300,  # 5 minutes
}

# Report configuration
REPORT_CONFIG = {
    "max_articles": 100,
    "cache_duration": 3600,  # 1 hour
} 