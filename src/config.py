"""
Configuration settings for the sentiment analysis pipeline.
"""

# RSS Feed URLs with fallback options
RSS_FEEDS = {
    'investing': 'https://www.investing.com/rss/news.rss',
    'marketwatch': 'https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines',
    'seeking_alpha': 'https://seekingalpha.com/feed.xml',
    'bloomberg_markets': 'https://www.bloomberg.com/feeds/sitemap_news.xml',
    'financial_times': 'https://www.ft.com/rss/markets'
}

# Rate limiting settings
RATE_LIMIT = {
    'requests_per_minute': 30,
    'retry_attempts': 3,
    'retry_delay': 5,  # seconds
    'timeout': 10  # seconds
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

# User agent for requests
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' 