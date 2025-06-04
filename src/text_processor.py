"""
Text preprocessing module for cleaning and normalizing article text.
"""

import re
import logging
from typing import Optional
from bs4 import BeautifulSoup
from .config import MIN_TEXT_LENGTH, MAX_TEXT_LENGTH

logger = logging.getLogger(__name__)

def clean_html(raw_html: str) -> str:
    """
    Remove HTML tags and extract clean text.
    
    Args:
        raw_html (str): Raw HTML content
        
    Returns:
        str: Cleaned text
    """
    try:
        soup = BeautifulSoup(raw_html, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and normalize whitespace
        text = soup.get_text(separator=' ', strip=True)
        return text
        
    except Exception as e:
        logger.error(f"Error cleaning HTML: {str(e)}")
        return raw_html

def preprocess_text(text: str) -> Optional[str]:
    """
    Preprocess text for sentiment analysis.
    
    Args:
        text (str): Input text
        
    Returns:
        Optional[str]: Preprocessed text or None if text is invalid
    """
    try:
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove special characters and numbers
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Check text length
        if len(text) < MIN_TEXT_LENGTH:
            logger.warning(f"Text too short ({len(text)} chars), skipping")
            return None
            
        if len(text) > MAX_TEXT_LENGTH:
            logger.warning(f"Text too long ({len(text)} chars), truncating")
            text = text[:MAX_TEXT_LENGTH]
            
        return text
        
    except Exception as e:
        logger.error(f"Error preprocessing text: {str(e)}")
        return None

def process_article(article: dict) -> Optional[dict]:
    """
    Process a single article's text.
    
    Args:
        article (dict): Article data
        
    Returns:
        Optional[dict]: Processed article or None if processing failed
    """
    try:
        # Clean HTML from summary
        cleaned_text = clean_html(article['summary'])
        
        # Preprocess text
        processed_text = preprocess_text(cleaned_text)
        
        if processed_text is None:
            return None
            
        # Update article with processed text
        article['processed_text'] = processed_text
        return article
        
    except Exception as e:
        logger.error(f"Error processing article: {str(e)}")
        return None 