"""
API package initialization.
"""
from flask import Blueprint

# Create API blueprint
api_bp = Blueprint('api', __name__)

# Import routes after blueprint creation to avoid circular imports
from . import market_routes, sentiment_routes, report_routes 