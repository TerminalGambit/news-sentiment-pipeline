"""
Tests for the text processor module.
"""

import pytest
from src.text_processor import clean_html, preprocess_text, process_article

def test_clean_html():
    """Test HTML cleaning functionality."""
    html = """
    <div class="article">
        <h1>Test Title</h1>
        <p>Test content with <a href="http://example.com">link</a></p>
        <script>var x = 1;</script>
        <style>.test { color: red; }</style>
    </div>
    """
    cleaned = clean_html(html)
    assert "Test Title" in cleaned
    assert "Test content with link" in cleaned
    assert "<script>" not in cleaned
    assert "<style>" not in cleaned
    assert "http://example.com" not in cleaned

def test_preprocess_text():
    """Test text preprocessing functionality."""
    text = "Test Article: $AAPL stock up 5% today! Visit https://example.com for more info."
    processed = preprocess_text(text)
    assert "test article" in processed.lower()
    assert "$aapl" in processed.lower()
    assert "https://example.com" not in processed
    assert len(processed) > 0

def test_process_article():
    """Test article processing functionality."""
    article = {
        'title': 'Test Article',
        'summary': '<p>Test content</p>',
        'link': 'http://example.com',
        'published': '2024-03-20T12:00:00Z',
        'source': 'Test Source'
    }
    processed = process_article(article)
    assert processed is not None
    assert 'text' in processed
    assert 'title' in processed
    assert 'source' in processed
    assert len(processed['text']) > 0

def test_process_article_invalid():
    """Test article processing with invalid input."""
    invalid_article = {
        'title': 'Test',
        'summary': ''
    }
    processed = process_article(invalid_article)
    assert processed is None 