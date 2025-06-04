"""
Configuration settings for the sentiment analysis pipeline.
"""

# RSS Feed URLs
RSS_FEEDS = {
    'yahoo_finance': 'https://finance.yahoo.com/news/rssindex',
    'cnbc': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'reuters': 'http://feeds.reuters.com/reuters/businessNews'
}

# Model settings
MODEL_NAME = "yiyanghkust/finbert-tone"
MAX_LENGTH = 512  # Maximum sequence length for the model

# File paths
DATA_DIR = "data"
RESULTS_FILE = f"{DATA_DIR}/sentiment_results.json"

# Sentiment labels mapping
SENTIMENT_LABELS = {
    'positive': 'Positive',
    'negative': 'Negative',
    'neutral': 'Neutral'
}

# Text preprocessing settings
MIN_TEXT_LENGTH = 50  # Minimum text length to process
MAX_TEXT_LENGTH = 1000  # Maximum text length to process 