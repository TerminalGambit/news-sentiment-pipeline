import os
import pytest
from src.market_data_pipeline import fetch_market_data

def test_fetch_market_data_format():
    ticker = "NVDA"
    data = fetch_market_data(ticker)
    assert data["error"] is None, f"API error: {data['error']}"
    assert isinstance(data["info"], dict), "Info should be a dict"
    assert isinstance(data["history"], list), "History should be a list"
    assert len(data["history"]) > 0, "History should not be empty"
    for row in data["history"]:
        assert isinstance(row, dict), "Each history row should be a dict"
        assert "Date" in row, "Each row should have a Date field"
        assert isinstance(row["Date"], str), "Date should be a string" 