"""
Sentiment analysis API routes.
"""
from flask import Blueprint, jsonify, request
from ..services.sentiment_service import SentimentService
from ..utils.logger import get_logger

logger = get_logger(__name__)
sentiment_bp = Blueprint("sentiment", __name__)
sentiment_service = SentimentService()

@sentiment_bp.route("/analyze", methods=["POST"])
def analyze_text():
    """Analyze sentiment of text."""
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400
        
        result = sentiment_service.analyze_text(data["text"])
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in analyze_text: {str(e)}")
        return jsonify({"error": str(e)}), 500

@sentiment_bp.route("/analyze/batch", methods=["POST"])
def analyze_batch():
    """Analyze sentiment of multiple texts."""
    try:
        data = request.get_json()
        if not data or "texts" not in data:
            return jsonify({"error": "No texts provided"}), 400
        
        results = sentiment_service.analyze_batch(data["texts"])
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in analyze_batch: {str(e)}")
        return jsonify({"error": str(e)}), 500

@sentiment_bp.route("/history", methods=["GET"])
def get_history():
    """Get sentiment analysis history."""
    try:
        results = sentiment_service.get_history()
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in get_history: {str(e)}")
        return jsonify({"error": str(e)}), 500

@sentiment_bp.route("/save", methods=["POST"])
def save_results():
    """Save sentiment analysis results."""
    try:
        data = request.get_json()
        if not data or "results" not in data:
            return jsonify({"error": "No results provided"}), 400
        
        sentiment_service.save_results(data["results"])
        return jsonify({"message": "Results saved successfully"})
    except Exception as e:
        logger.error(f"Error in save_results: {str(e)}")
        return jsonify({"error": str(e)}), 500 