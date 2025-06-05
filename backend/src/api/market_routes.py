"""
Market data API routes.
"""
from flask import Blueprint, jsonify, request
from ..services.market_service import MarketService
from ..utils.logger import get_logger

logger = get_logger(__name__)
market_bp = Blueprint("market", __name__)
market_service = MarketService()

@market_bp.route("/overview", methods=["GET"])
def get_market_overview():
    """Get market overview for all symbols."""
    try:
        overview = market_service.get_market_overview()
        return jsonify(overview)
    except Exception as e:
        logger.error(f"Error in get_market_overview: {str(e)}")
        return jsonify({"error": str(e)}), 500

@market_bp.route("/data/<symbol>", methods=["GET"])
def get_market_data(symbol):
    """Get market data for a specific symbol."""
    try:
        timeframe = request.args.get("timeframe", "1mo")
        period = request.args.get("period", "1y")
        
        data = market_service.get_market_data(symbol, timeframe, period)
        if not data:
            return jsonify({"error": f"No data found for {symbol}"}), 404
        
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in get_market_data for {symbol}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@market_bp.route("/symbols", methods=["GET"])
def get_symbols():
    """Get list of available symbols."""
    try:
        return jsonify({"symbols": market_service.symbols})
    except Exception as e:
        logger.error(f"Error in get_symbols: {str(e)}")
        return jsonify({"error": str(e)}), 500

@market_bp.route("/timeframes", methods=["GET"])
def get_timeframes():
    """Get list of available timeframes."""
    try:
        return jsonify({"timeframes": market_service.timeframes})
    except Exception as e:
        logger.error(f"Error in get_timeframes: {str(e)}")
        return jsonify({"error": str(e)}), 500 