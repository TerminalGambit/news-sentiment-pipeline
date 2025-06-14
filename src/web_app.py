"""
Web application for displaying sentiment analysis reports.
"""

# pylint: disable=import-error
import json
import os
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template

from .config import DATA_DIR
from .report_generator import ReportGenerator
from .storage import DataStorage
from .market_data_pipeline import fetch_market_data, get_market_dataframe
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)

# Initialize components
report_generator = ReportGenerator()
data_storage = DataStorage()

def format_number(value):
    """Format number with appropriate suffix (K, M, B) and decimal places."""
    if value is None:
        return "N/A"
    
    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)
    
    if abs(value) >= 1e12:  # Trillion
        return f"${value/1e12:.2f}T"
    elif abs(value) >= 1e9:  # Billion
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:  # Million
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:  # Thousand
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

# Register the custom filter
app.jinja_env.filters['format_number'] = format_number

def get_available_reports() -> List[str]:
    """Get list of available report dates."""
    reports_dir = os.path.join(DATA_DIR, "reports")
    if not os.path.exists(reports_dir):
        return []
    return sorted(
        [
            d
            for d in os.listdir(reports_dir)
            if os.path.isdir(os.path.join(reports_dir, d))
        ],
        reverse=True,
    )


@app.route("/")
def index():
    """Render the main page with list of available reports."""
    reports = get_available_reports()
    return render_template("index.html", reports=reports)


@app.route("/report/<date>")
def view_report(date: str):
    """Render a specific report."""
    report_dir = os.path.join(DATA_DIR, "reports", date)
    if not os.path.exists(report_dir):
        return "Report not found", 404

    # Load report data from main results file
    results_file = os.path.join(DATA_DIR, "sentiment_results.json")
    if os.path.exists(results_file):
        with open(results_file, "r", encoding="utf-8") as f:
            results = json.load(f)
    else:
        results = []

    # Get report metadata
    report_data = {
        "date": date,
        "total_articles": len(results),
        "sources": sorted(set(article["source"] for article in results)),
        "sentiment_distribution": get_sentiment_distribution(results),
        "source_stats": get_source_stats(results),
        "top_positive": get_top_articles(results, "Positive"),
        "top_negative": get_top_articles(results, "Negative"),
    }

    return render_template("report.html", report=report_data)


@app.route("/api/report/<date>")
def get_report_data(date: str):
    """Get report data as JSON."""
    cache_file = os.path.join(DATA_DIR, "cache", f"results_{date}.json")
    if not os.path.exists(cache_file):
        return jsonify({"error": "Report not found"}), 404

    with open(cache_file, "r", encoding="utf-8") as f:
        results = json.load(f)

    return jsonify(
        {
            "date": date,
            "total_articles": len(results),
            "sources": sorted(set(article["source"] for article in results)),
            "sentiment_distribution": get_sentiment_distribution(results),
            "source_stats": get_source_stats(results),
            "top_positive": get_top_articles(results, "Positive"),
            "top_negative": get_top_articles(results, "Negative"),
        }
    )


def get_sentiment_distribution(results: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calculate sentiment distribution."""
    distribution = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for result in results:
        label = result["sentiment"]["label"]
        distribution[label] += 1
    return distribution


def get_source_stats(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Calculate statistics by source."""
    stats = {}
    for article in results:
        source = article["source"]
        sentiment = article["sentiment"]["label"]

        if source not in stats:
            stats[source] = {"positive": 0, "neutral": 0, "negative": 0}

        stats[source][sentiment.lower()] += 1
    return stats


def get_top_articles(
    results: List[Dict[str, Any]], sentiment: str, limit: int = 5
) -> List[Dict[str, Any]]:
    """Get top articles by sentiment."""
    return sorted(
        [r for r in results if r["sentiment"]["label"] == sentiment],
        key=lambda x: x["sentiment"]["score"],
        reverse=True,
    )[:limit]


@app.route("/report/<date>/positive")
def see_all_positive(date: str):
    results_file = os.path.join(DATA_DIR, "sentiment_results.json")
    if os.path.exists(results_file):
        with open(results_file, "r", encoding="utf-8") as f:
            results = json.load(f)
    else:
        results = []
    positive_articles = [r for r in results if r["sentiment"]["label"] == "Positive"]
    positive_articles = sorted(positive_articles, key=lambda x: x["sentiment"]["score"], reverse=True)
    return render_template("see_all_positive.html", date=date, articles=positive_articles)


@app.route("/report/<date>/negative")
def see_all_negative(date: str):
    results_file = os.path.join(DATA_DIR, "sentiment_results.json")
    if os.path.exists(results_file):
        with open(results_file, "r", encoding="utf-8") as f:
            results = json.load(f)
    else:
        results = []
    negative_articles = [r for r in results if r["sentiment"]["label"] == "Negative"]
    negative_articles = sorted(negative_articles, key=lambda x: x["sentiment"]["score"], reverse=True)
    return render_template("see_all_negative.html", date=date, articles=negative_articles)


@app.route("/market/<ticker>")
def market_overview(ticker):
    data = fetch_market_data(ticker)
    error = data.get("error")
    info = data.get("info")
    df = get_market_dataframe(data)
    price_data = None
    if not error and not df.empty:
        price_data = {
            "dates": df["Date"].tolist(),
            "close": df["Close"].tolist(),
            "open": df["Open"].tolist(),
            "high": df["High"].tolist(),
            "low": df["Low"].tolist(),
            "volume": df["Volume"].tolist(),
        }
    return render_template(
        "market_overview.html",
        ticker=ticker,
        info=info,
        error=error,
        price_data=price_data,
        df=df.to_dict(orient="records") if not df.empty else None
    )


@app.route("/market/<ticker>/sma")
def market_sma(ticker):
    data = fetch_market_data(ticker)
    error = data.get("error")
    info = data.get("info")
    df = get_market_dataframe(data)
    sma_data = None
    if not error and not df.empty:
        df["SMA20"] = df["Close"].rolling(window=20).mean()
        df["SMA50"] = df["Close"].rolling(window=50).mean()
        sma_data = {
            "dates": df["Date"].tolist(),
            "close": df["Close"].tolist(),
            "sma20": df["SMA20"].tolist(),
            "sma50": df["SMA50"].tolist(),
        }
    return render_template(
        "market_sma.html",
        ticker=ticker,
        info=info,
        error=error,
        sma_data=sma_data,
        df=df.to_dict(orient="records") if not df.empty else None
    )


@app.route("/market/<ticker>/rsi")
def market_rsi(ticker):
    data = fetch_market_data(ticker)
    error = data.get("error")
    info = data.get("info")
    df = get_market_dataframe(data)
    rsi_data = None
    if not error and not df.empty:
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        df["RSI14"] = rsi
        rsi_data = {
            "dates": df["Date"].tolist(),
            "close": df["Close"].tolist(),
            "rsi14": df["RSI14"].tolist(),
        }
    return render_template(
        "market_rsi.html",
        ticker=ticker,
        info=info,
        error=error,
        rsi_data=rsi_data,
        df=df.to_dict(orient="records") if not df.empty else None
    )


@app.route("/market/<ticker>/macd")
def market_macd(ticker):
    data = fetch_market_data(ticker)
    error = data.get("error")
    info = data.get("info")
    df = get_market_dataframe(data)
    macd_data = None
    if not error and not df.empty:
        ema12 = df["Close"].ewm(span=12, adjust=False).mean()
        ema26 = df["Close"].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        df["MACD"] = macd
        df["MACDSignal"] = signal
        macd_data = {
            "dates": df["Date"].tolist(),
            "close": df["Close"].tolist(),
            "macd": df["MACD"].tolist(),
            "signal": df["MACDSignal"].tolist(),
        }
    return render_template(
        "market_macd.html",
        ticker=ticker,
        info=info,
        error=error,
        macd_data=macd_data,
        df=df.to_dict(orient="records") if not df.empty else None
    )


def run_web_app(host: str = "127.0.0.1", port: int = 5000, debug: bool = True):
    """Run the Flask web application."""
    app.run(host=host, port=port, debug=debug)
