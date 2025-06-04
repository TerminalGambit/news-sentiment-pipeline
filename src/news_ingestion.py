"""
News ingestion module for fetching financial news from RSS feeds.
"""

import feedparser
import logging
from typing import List, Dict, Any
from datetime import datetime
import requests
from tqdm import tqdm

from .config import RSS_FEEDS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fetch_rss_articles(feed_url: str, timeout: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch articles from an RSS feed with error handling and timeout.
    
    Args:
        feed_url (str): URL of the RSS feed
        timeout (int): Request timeout in seconds
        
    Returns:
        List[Dict[str, Any]]: List of article entries
    """
    try:
        # Verify feed URL is accessible
        response = requests.head(feed_url, timeout=timeout)
        response.raise_for_status()
        
        # Parse feed
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:  # Check for feed parsing errors
            logger.warning(f"Feed parsing issues for {feed_url}: {feed.bozo_exception}")
        
        articles = []
        for entry in feed.entries:
            article = {
                'title': entry.get('title', ''),
                'summary': entry.get('summary', ''),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'source': feed_url,
                'timestamp': datetime.now().isoformat()
            }
            articles.append(article)
            
        logger.info(f"Successfully fetched {len(articles)} articles from {feed_url}")
        return articles
        
    except requests.RequestException as e:
        logger.error(f"Failed to fetch feed {feed_url}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching feed {feed_url}: {str(e)}")
        return []

def fetch_all_feeds() -> List[Dict[str, Any]]:
    """
    Fetch articles from all configured RSS feeds.
    
    Returns:
        List[Dict[str, Any]]: Combined list of articles from all feeds
    """
    all_articles = []
    
    for source, url in tqdm(RSS_FEEDS.items(), desc="Fetching feeds"):
        articles = fetch_rss_articles(url)
        all_articles.extend(articles)
        
    logger.info(f"Total articles fetched: {len(all_articles)}")
    return all_articles 