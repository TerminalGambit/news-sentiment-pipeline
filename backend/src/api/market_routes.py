"""
Market data API routes.
"""
from flask import jsonify, request
from ..services.market_service import MarketService
from ..utils.response import create_response

market_service = MarketService()

@api_bp.route('/api/market/<ticker>', methods=['GET'])
def get_market_overview(ticker):
    """Get market overview data for a ticker."""
    try:
        data = market_service.get_market_data(ticker)
        return create_response(data=data)
    except Exception as e:
        return create_response(error=str(e)), 400

@api_bp.route('/api/market/<ticker>/sma', methods=['GET'])
def get_sma_data(ticker):
    """Get SMA data for a ticker."""
    try:
        data = market_service.get_sma_data(ticker)
        return create_response(data=data)
    except Exception as e:
        return create_response(error=str(e)), 400

@api_bp.route('/api/market/<ticker>/rsi', methods=['GET'])
def get_rsi_data(ticker):
    """Get RSI data for a ticker."""
    try:
        data = market_service.get_rsi_data(ticker)
        return create_response(data=data)
    except Exception as e:
        return create_response(error=str(e)), 400

@api_bp.route('/api/market/<ticker>/macd', methods=['GET'])
def get_macd_data(ticker):
    """Get MACD data for a ticker."""
    try:
        data = market_service.get_macd_data(ticker)
        return create_response(data=data)
    except Exception as e:
        return create_response(error=str(e)), 400 