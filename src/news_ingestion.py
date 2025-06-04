"""
News ingestion module for fetching financial news from RSS feeds.
"""

import logging
import random
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import feedparser
import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

from .config import RATE_LIMIT, RSS_FEEDS, USER_AGENT

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for API requests."""

    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.interval = 60.0 / requests_per_minute
        self.last_request = 0.0

    def wait(self):
        """Wait if necessary to respect rate limits."""
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_request = time.time()


class NewsFetcher:
    """Class to handle news fetching with retries and rate limiting."""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.session = self._create_session()
        self.rate_limiter = RateLimiter(RATE_LIMIT["requests_per_minute"])

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=RATE_LIMIT["retry_attempts"],
            backoff_factor=RATE_LIMIT["retry_delay"],
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({"User-Agent": USER_AGENT})
        return session

    def fetch_feed(self, feed_url: str) -> Optional[feedparser.FeedParserDict]:
        """
        Fetch a single RSS feed with rate limiting and retries.

        Args:
            feed_url (str): URL of the RSS feed

        Returns:
            Optional[feedparser.FeedParserDict]: Parsed feed or None if failed
        """
        try:
            self.rate_limiter.wait()
            response = self.session.get(feed_url, timeout=RATE_LIMIT["timeout"])
            response.raise_for_status()

            # Add random delay to avoid detection
            time.sleep(random.uniform(1, 3))

            feed = feedparser.parse(response.content)
            if feed.bozo:
                logger.warning(
                    "Feed parsing issues for %s: %s", feed_url, feed.bozo_exception
                )

            return feed

        except requests.RequestException as e:
            logger.error("Failed to fetch feed %s: %s", feed_url, str(e))
            return None
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Unexpected error fetching feed %s: %s", feed_url, str(e))
            return None

    def process_feed(
        self, feed: feedparser.FeedParserDict, source: str
    ) -> List[Dict[str, Any]]:
        """
        Process a feed and extract articles.

        Args:
            feed (feedparser.FeedParserDict): Parsed feed
            source (str): Source name

        Returns:
            List[Dict[str, Any]]: List of processed articles
        """
        articles = []
        for entry in feed.entries:
            try:
                article = {
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": source,
                    "timestamp": datetime.now().isoformat(),
                }
                articles.append(article)
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error processing article from %s: %s", source, str(e))
                continue
        return articles


def fetch_rss_articles(feed_url: str, source: str) -> List[Dict[str, Any]]:
    """
    Fetch articles from an RSS feed with error handling and rate limiting.

    Args:
        feed_url (str): URL of the RSS feed
        source (str): Source name

    Returns:
        List[Dict[str, Any]]: List of article entries
    """
    fetcher = NewsFetcher()
    feed = fetcher.fetch_feed(feed_url)

    if feed is None:
        return []

    articles = fetcher.process_feed(feed, source)
    logger.info(f"Successfully fetched {len(articles)} articles from {source}")
    return articles


def fetch_all_feeds() -> List[Dict[str, Any]]:
    """
    Fetch articles from all configured RSS feeds.

    Returns:
        List[Dict[str, Any]]: Combined list of articles from all feeds
    """
    all_articles = []
    fetcher = NewsFetcher()

    for source, url in tqdm(RSS_FEEDS.items(), desc="Fetching feeds"):
        try:
            feed = fetcher.fetch_feed(url)
            if feed:
                articles = fetcher.process_feed(feed, source)
                all_articles.extend(articles)
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error processing feed %s: %s", source, str(e))
            continue

    logger.info("Total articles fetched: %d", len(all_articles))
    return all_articles
