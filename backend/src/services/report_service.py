"""
Report generation and retrieval service.
"""
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
from ..utils.logger import get_logger
from ..config import DATA_DIR

logger = get_logger(__name__)

class ReportService:
    """Service for handling report operations."""
    
    def __init__(self):
        """Initialize the report service."""
        self.reports_dir = os.path.join(DATA_DIR, "reports")
        self.results_file = os.path.join(DATA_DIR, "sentiment_results.json")
    
    def get_available_reports(self) -> List[str]:
        """
        Get list of available report dates.
        
        Returns:
            List of report dates
        """
        try:
            if not os.path.exists(self.reports_dir):
                return []
            
            return sorted(
                [
                    d
                    for d in os.listdir(self.reports_dir)
                    if os.path.isdir(os.path.join(self.reports_dir, d))
                ],
                reverse=True,
            )
        except Exception as e:
            logger.error(f"Error getting available reports: {str(e)}")
            raise
    
    def get_report(self, date: str) -> Optional[Dict[str, Any]]:
        """
        Get specific report by date.
        
        Args:
            date: Report date
            
        Returns:
            Dict containing report data
        """
        try:
            report_dir = os.path.join(self.reports_dir, date)
            if not os.path.exists(report_dir):
                return None
            
            # Load report data from main results file
            if os.path.exists(self.results_file):
                with open(self.results_file, "r", encoding="utf-8") as f:
                    results = json.load(f)
            else:
                results = []
            
            # Get report metadata
            return {
                "date": date,
                "total_articles": len(results),
                "sources": sorted(set(article["source"] for article in results)),
                "sentiment_distribution": self._get_sentiment_distribution(results),
                "source_stats": self._get_source_stats(results),
                "top_positive": self._get_top_articles(results, "Positive"),
                "top_negative": self._get_top_articles(results, "Negative"),
            }
        except Exception as e:
            logger.error(f"Error getting report for {date}: {str(e)}")
            raise
    
    def get_positive_articles(self, date: str) -> List[Dict[str, Any]]:
        """
        Get positive articles for a specific report.
        
        Args:
            date: Report date
            
        Returns:
            List of positive articles
        """
        try:
            if not os.path.exists(self.results_file):
                return []
            
            with open(self.results_file, "r", encoding="utf-8") as f:
                results = json.load(f)
            
            positive_articles = [
                r for r in results
                if r["sentiment"]["label"] == "Positive"
            ]
            return sorted(
                positive_articles,
                key=lambda x: x["sentiment"]["score"],
                reverse=True
            )
        except Exception as e:
            logger.error(f"Error getting positive articles for {date}: {str(e)}")
            raise
    
    def get_negative_articles(self, date: str) -> List[Dict[str, Any]]:
        """
        Get negative articles for a specific report.
        
        Args:
            date: Report date
            
        Returns:
            List of negative articles
        """
        try:
            if not os.path.exists(self.results_file):
                return []
            
            with open(self.results_file, "r", encoding="utf-8") as f:
                results = json.load(f)
            
            negative_articles = [
                r for r in results
                if r["sentiment"]["label"] == "Negative"
            ]
            return sorted(
                negative_articles,
                key=lambda x: x["sentiment"]["score"],
                reverse=True
            )
        except Exception as e:
            logger.error(f"Error getting negative articles for {date}: {str(e)}")
            raise
    
    def _get_sentiment_distribution(self, results: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate sentiment distribution.
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            Dict containing sentiment distribution
        """
        distribution = {"Positive": 0, "Neutral": 0, "Negative": 0}
        for result in results:
            label = result["sentiment"]["label"]
            distribution[label] += 1
        return distribution
    
    def _get_source_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
        """
        Calculate statistics by source.
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            Dict containing source statistics
        """
        stats = {}
        for article in results:
            source = article["source"]
            sentiment = article["sentiment"]["label"]
            
            if source not in stats:
                stats[source] = {"positive": 0, "neutral": 0, "negative": 0}
            
            stats[source][sentiment.lower()] += 1
        return stats
    
    def _get_top_articles(
        self,
        results: List[Dict[str, Any]],
        sentiment: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get top articles by sentiment.
        
        Args:
            results: List of sentiment analysis results
            sentiment: Sentiment label
            limit: Maximum number of articles to return
            
        Returns:
            List of top articles
        """
        return sorted(
            [r for r in results if r["sentiment"]["label"] == sentiment],
            key=lambda x: x["sentiment"]["score"],
            reverse=True
        )[:limit] 