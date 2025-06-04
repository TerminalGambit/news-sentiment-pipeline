"""
Web application for displaying sentiment analysis reports.
"""

from flask import Flask, render_template, jsonify, send_file
import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config import DATA_DIR
from .report_generator import ReportGenerator
from .storage import DataStorage

app = Flask(__name__)

# Initialize components
report_generator = ReportGenerator()
data_storage = DataStorage()

def get_available_reports() -> List[str]:
    """Get list of available report dates."""
    reports_dir = os.path.join(DATA_DIR, "reports")
    if not os.path.exists(reports_dir):
        return []
    return sorted([d for d in os.listdir(reports_dir) if os.path.isdir(os.path.join(reports_dir, d))], reverse=True)

@app.route('/')
def index():
    """Render the main page with list of available reports."""
    reports = get_available_reports()
    return render_template('index.html', reports=reports)

@app.route('/report/<date>')
def view_report(date: str):
    """Render a specific report."""
    report_dir = os.path.join(DATA_DIR, "reports", date)
    if not os.path.exists(report_dir):
        return "Report not found", 404
        
    # Load report data
    cache_file = os.path.join(DATA_DIR, "cache", f"results_{date}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            results = json.load(f)
    else:
        results = []
        
    # Get report metadata
    report_data = {
        'date': date,
        'total_articles': len(results),
        'sources': sorted(set(article['source'] for article in results)),
        'sentiment_distribution': get_sentiment_distribution(results),
        'source_stats': get_source_stats(results),
        'top_positive': get_top_articles(results, 'Positive'),
        'top_negative': get_top_articles(results, 'Negative')
    }
    
    return render_template('report.html', report=report_data)

@app.route('/api/report/<date>')
def get_report_data(date: str):
    """Get report data as JSON."""
    cache_file = os.path.join(DATA_DIR, "cache", f"results_{date}.json")
    if not os.path.exists(cache_file):
        return jsonify({'error': 'Report not found'}), 404
        
    with open(cache_file, 'r') as f:
        results = json.load(f)
        
    return jsonify({
        'date': date,
        'total_articles': len(results),
        'sources': sorted(set(article['source'] for article in results)),
        'sentiment_distribution': get_sentiment_distribution(results),
        'source_stats': get_source_stats(results),
        'top_positive': get_top_articles(results, 'Positive'),
        'top_negative': get_top_articles(results, 'Negative')
    })

def get_sentiment_distribution(results: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calculate sentiment distribution."""
    distribution = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    for result in results:
        label = result['sentiment']['label']
        distribution[label] += 1
    return distribution

def get_source_stats(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Calculate statistics by source."""
    stats = {}
    for article in results:
        source = article['source']
        sentiment = article['sentiment']['label']
        
        if source not in stats:
            stats[source] = {'positive': 0, 'neutral': 0, 'negative': 0}
            
        stats[source][sentiment.lower()] += 1
    return stats

def get_top_articles(results: List[Dict[str, Any]], sentiment: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Get top articles by sentiment."""
    return sorted(
        [r for r in results if r['sentiment']['label'] == sentiment],
        key=lambda x: x['sentiment']['score'],
        reverse=True
    )[:limit]

def run_web_app(host: str = '127.0.0.1', port: int = 5000, debug: bool = True):
    """Run the Flask web application."""
    app.run(host=host, port=port, debug=debug) 