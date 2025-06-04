"""
Text preprocessing module for cleaning and normalizing article text.
"""

import logging
import re
import unicodedata
from datetime import datetime
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup

from .config import MAX_TEXT_LENGTH, MIN_TEXT_LENGTH

logger = logging.getLogger(__name__)

# Common financial terms and their normalized forms
FINANCIAL_TERMS = {
    "usd": "USD",
    "eur": "EUR",
    "gbp": "GBP",
    "jpy": "JPY",
    "cny": "CNY",
    "btc": "BTC",
    "eth": "ETH",
    "nasdaq": "NASDAQ",
    "nyse": "NYSE",
    "ftse": "FTSE",
    "dow": "Dow Jones",
    "s&p": "S&P",
    "fed": "Federal Reserve",
    "ecb": "European Central Bank",
    "boe": "Bank of England",
    "boj": "Bank of Japan",
    "pboc": "People's Bank of China",
}


def clean_html(raw_html: str) -> str:
    """
    Remove HTML tags and extract clean text with improved handling.

    Args:
        raw_html (str): Raw HTML content

    Returns:
        str: Cleaned text
    """
    try:
        soup = BeautifulSoup(raw_html, "html.parser")

        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        # Remove comments
        for comment in soup.find_all(
            text=lambda text: isinstance(text, str) and text.strip().startswith("<!--")
        ):
            comment.extract()

        # Get text and normalize whitespace
        text = soup.get_text(separator=" ", strip=True)

        # Remove multiple spaces and newlines
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    except Exception as e:
        logger.error("Error cleaning HTML: %s", str(e))
        return raw_html


def normalize_financial_terms(text: str) -> str:
    """
    Normalize common financial terms and symbols.
    """
    for term, replacement in FINANCIAL_TERMS.items():
        pattern = r"\\b" + re.escape(term) + r"\\b"
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def remove_noise(text: str) -> str:
    """
    Remove noise from text (ads, disclaimers, etc.).

    Args:
        text (str): Input text

    Returns:
        str: Cleaned text
    """
    # Remove common ad phrases
    ad_patterns = [
        r"click here to read more",
        r"subscribe to our newsletter",
        r"follow us on",
        r"like us on facebook",
        r"follow us on twitter",
        r"disclaimer:",
        r"terms of use:",
        r"privacy policy:",
        r"copyright ©",
        r"all rights reserved",
    ]

    for pattern in ad_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return text


def preprocess_text(text: str) -> Optional[str]:
    """
    Preprocess text for sentiment analysis with financial-specific handling.

    Args:
        text (str): Input text

    Returns:
        Optional[str]: Preprocessed text or None if text is invalid
    """
    try:
        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

        # Remove email addresses
        text = re.sub(r"\S+@\S+", "", text)

        # Remove special characters but keep important ones
        text = re.sub(r"[^\w\s.,$%€£¥+-]", " ", text)

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        # Remove noise
        text = remove_noise(text)

        # Normalize financial terms
        text = normalize_financial_terms(text)

        # Normalize unicode characters
        text = unicodedata.normalize("NFKD", text)

        # Check text length
        if len(text) < MIN_TEXT_LENGTH:
            logger.warning("Text too short (%d chars), skipping", len(text))
            return None

        if len(text) > MAX_TEXT_LENGTH:
            logger.warning("Text too long (%d chars), truncating", len(text))
            text = text[:MAX_TEXT_LENGTH]

        return text

    except Exception as e:
        logger.error("Error preprocessing text: %s", str(e))
        return None


def process_article(article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process a single article's text with enhanced error handling.

    Args:
        article (Dict[str, Any]): Article data

    Returns:
        Optional[Dict[str, Any]]: Processed article or None if processing failed
    """
    try:
        # Validate article structure
        required_fields = ["title", "summary", "link", "source"]
        if not all(field in article for field in required_fields):
            logger.error(f"Article missing required fields: {required_fields}")
            return None

        # Clean HTML from summary
        cleaned_text = clean_html(article["summary"])

        # Combine title and summary for better context
        combined_text = f"{article['title']} {cleaned_text}"

        # Preprocess text
        processed_text = preprocess_text(combined_text)

        if processed_text is None:
            return None

        # Update article with processed text and metadata
        article["processed_text"] = processed_text
        article["processed_at"] = datetime.now().isoformat()
        article["text_length"] = len(processed_text)

        return article

    except Exception as e:
        logger.error("Error processing article: %s", str(e))
        return None
