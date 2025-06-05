"""
Report generation and retrieval API routes.
"""
from flask import Blueprint, jsonify, request
from ..services.report_service import ReportService
from ..utils.logger import get_logger

logger = get_logger(__name__)
report_bp = Blueprint("report", __name__)
report_service = ReportService()

@report_bp.route("/reports", methods=["GET"])
def get_available_reports():
    """Get list of available reports."""
    try:
        reports = report_service.get_available_reports()
        return jsonify({"reports": reports})
    except Exception as e:
        logger.error(f"Error in get_available_reports: {str(e)}")
        return jsonify({"error": str(e)}), 500

@report_bp.route("/reports/<date>", methods=["GET"])
def get_report(date):
    """Get specific report by date."""
    try:
        report = report_service.get_report(date)
        if not report:
            return jsonify({"error": f"No report found for {date}"}), 404
        
        return jsonify(report)
    except Exception as e:
        logger.error(f"Error in get_report for {date}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@report_bp.route("/reports/<date>/positive", methods=["GET"])
def get_positive_articles(date):
    """Get positive articles for a specific report."""
    try:
        articles = report_service.get_positive_articles(date)
        return jsonify({"articles": articles})
    except Exception as e:
        logger.error(f"Error in get_positive_articles for {date}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@report_bp.route("/reports/<date>/negative", methods=["GET"])
def get_negative_articles(date):
    """Get negative articles for a specific report."""
    try:
        articles = report_service.get_negative_articles(date)
        return jsonify({"articles": articles})
    except Exception as e:
        logger.error(f"Error in get_negative_articles for {date}: {str(e)}")
        return jsonify({"error": str(e)}), 500 