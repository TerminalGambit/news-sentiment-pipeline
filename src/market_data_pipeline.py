import os
import time
import json
import pandas as pd
import yfinance as yf
import logging
from datetime import datetime

CACHE_DIR = "data/market_cache"
CACHE_EXPIRY = 60 * 60  # 1 hour
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "market_api_requests.log")

def ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)

def cache_path(ticker):
    return os.path.join(CACHE_DIR, f"{ticker.upper()}_data.json")

def is_cache_valid(path):
    if not os.path.exists(path):
        return False
    mtime = os.path.getmtime(path)
    return (time.time() - mtime) < CACHE_EXPIRY

def ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)

def log_api_request(ticker, result):
    ensure_log_dir()
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {ticker} | {result}\n")

def fetch_market_data(ticker):
    """
    Fetch and cache market data for a given ticker using yfinance.
    Returns a dict with info, history, and error (if any).
    Automatically clears bad cache if error is detected.
    Logs every API request.
    """
    ensure_cache_dir()
    cache_file = cache_path(ticker)
    # If cache exists and is invalid (error), clear it
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            try:
                cached = json.load(f)
                if cached.get("error") and (cached.get("info") is None or cached.get("history") is None):
                    os.remove(cache_file)
            except Exception:
                os.remove(cache_file)
    if is_cache_valid(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1y").reset_index()
        # Convert Timestamp to string for JSON serialization
        if 'Date' in hist.columns:
            hist['Date'] = hist['Date'].astype(str)
        hist_records = hist.to_dict(orient="records")
        data = {"info": info, "history": hist_records, "error": None}
        with open(cache_file, "w") as f:
            json.dump(data, f)
        log_api_request(ticker, "success")
        return data
    except Exception as e:
        # Handle API errors, including rate limits
        error_msg = str(e)
        data = {"info": None, "history": None, "error": error_msg}
        with open(cache_file, "w") as f:
            json.dump(data, f)
        log_api_request(ticker, f"error: {error_msg}")
        return data

def get_market_dataframe(data):
    if data["history"]:
        return pd.DataFrame(data["history"])
    return pd.DataFrame()

if __name__ == "__main__":
    ticker = "NVDA"  # NVIDIA for proof of concept
    data = fetch_market_data(ticker)
    if data["error"]:
        print(f"Error fetching data for {ticker}: {data['error']}")
    else:
        print(f"Fetched info for {ticker}: {data['info'].get('longName', ticker)}")
        df = get_market_dataframe(data)
        print(df.head()) 