"""
Main application module.
"""
from flask import Flask
from flask_cors import CORS
from .api.market_routes import market_bp
from .api.sentiment_routes import sentiment_bp
from .api.report_routes import report_bp
from .utils.logger import get_logger

logger = get_logger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(market_bp, url_prefix="/api/market")
    app.register_blueprint(sentiment_bp, url_prefix="/api/sentiment")
    app.register_blueprint(report_bp, url_prefix="/api/report")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Server error: {str(error)}")
        return {"error": "Internal server error"}, 500
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) 