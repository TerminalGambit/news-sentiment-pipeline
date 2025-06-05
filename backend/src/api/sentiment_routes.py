"""
Sentiment analysis API routes.
"""
from flask import jsonify, request
from ..services.sentiment_service import SentimentService
from ..utils.response import create_response

sentiment_service = SentimentService()

@api_bp.route('/api/sentiment/analyze', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment for provided text."""
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return create_response(error="No text provided"), 400
        
        result = sentiment_service.analyze_text(text)
        return create_response(data=result)
    except Exception as e:
        return create_response(error=str(e)), 400

@api_bp.route('/api/sentiment/batch', methods=['POST'])
def analyze_batch():
    """Analyze sentiment for multiple texts."""
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        if not texts:
            return create_response(error="No texts provided"), 400
        
        results = sentiment_service.analyze_batch(texts)
        return create_response(data=results)
    except Exception as e:
        return create_response(error=str(e)), 400

@api_bp.route('/api/sentiment/history', methods=['GET'])
def get_sentiment_history():
    """Get sentiment analysis history."""
    try:
        results = sentiment_service.get_history()
        return create_response(data=results)
    except Exception as e:
        return create_response(error=str(e)), 400 