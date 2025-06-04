"""
Main pipeline module for orchestrating the sentiment analysis process.
"""

import logging
import time
from typing import Any, Dict, List

from .news_ingestion import fetch_all_feeds
from .report_generator import ReportGenerator
from .sentiment_analyzer import SentimentAnalyzer
from .storage import DataStorage
from .text_processor import process_article

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SentimentAnalysisPipeline:
    """Pipeline for orchestrating the sentiment analysis process."""

    def __init__(self):
        """Initialize the pipeline components."""
        self.analyzer = SentimentAnalyzer()
        self.storage = DataStorage()
        self.report_generator = ReportGenerator()

    def run(
        self, save_csv: bool = True, generate_report: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Run the complete sentiment analysis pipeline.
        """
        start_time = time.time()
        logger.info("Starting sentiment analysis pipeline")
        try:
            logger.info("Fetching news articles...")
            articles = fetch_all_feeds()
            if not articles:
                logger.warning("No articles fetched, ending pipeline")
                return []
            logger.info("Processing articles...")
            processed_articles = [
                process_article(article)
                for article in articles
                if process_article(article)
            ]
            if not processed_articles:
                logger.warning("No articles processed successfully, ending pipeline")
                return []
            logger.info("Analyzing sentiment...")
            results = self.analyzer.analyze_articles(processed_articles)
            logger.info("Saving results...")
            self.storage.save_to_json(results)
            if save_csv:
                self.storage.save_to_csv(results)
            if generate_report:
                logger.info("Generating report...")
                report_path = self.report_generator.generate_report(results)
                logger.info("Report generated: %s", report_path)
            duration = time.time() - start_time
            logger.info("Pipeline completed in %.2f seconds", duration)
            logger.info("Processed %d articles", len(results))
            sentiment_counts = {}
            for result in results:
                label = result["sentiment"]["label"]
                sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
            logger.info("Sentiment distribution:")
            for label, count in sentiment_counts.items():
                logger.info("%s: %d articles", label, count)
            return results
        except Exception as e:
            logger.error("Pipeline failed: %s", str(e))
            return []


def main():
    """Main entry point for the pipeline."""
    pipeline = SentimentAnalysisPipeline()
    pipeline.run()


if __name__ == "__main__":
    main()
