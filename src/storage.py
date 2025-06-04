"""
Data storage module for saving sentiment analysis results.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from .config import DATA_DIR, RESULTS_FILE

logger = logging.getLogger(__name__)


class DataStorage:
    """Class for saving and loading sentiment analysis results in JSON and CSV formats."""

    def __init__(self):
        """Initialize data storage with directory creation."""
        os.makedirs(DATA_DIR, exist_ok=True)

    def save_to_json(
        self, data: List[Dict[str, Any]], filename: str = RESULTS_FILE
    ) -> bool:
        """
        Save results to JSON file.

        Args:
            data (List[Dict[str, Any]]): Data to save
            filename (str): Output filename

        Returns:
            bool: Success status
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Successfully saved %d records to %s", len(data), filename)
            return True
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error saving to JSON: %s", str(e))
            return False

    def save_to_csv(self, data: List[Dict[str, Any]], filename: str = None) -> bool:
        """
        Save results to CSV file.

        Args:
            data (List[Dict[str, Any]]): Data to save
            filename (str): Output filename (optional)

        Returns:
            bool: Success status
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{DATA_DIR}/sentiment_results_{timestamp}.csv"

            # Convert to DataFrame for easier handling
            df = pd.DataFrame(data)

            # Flatten nested sentiment dictionary
            if "sentiment" in df.columns:
                df["sentiment_label"] = df["sentiment"].apply(
                    lambda x: x.get("label", "")
                )
                df["sentiment_score"] = df["sentiment"].apply(
                    lambda x: x.get("score", 0)
                )
                df = df.drop("sentiment", axis=1)

            # Save to CSV
            df.to_csv(filename, index=False, encoding="utf-8")
            logger.info("Successfully saved %d records to %s", len(data), filename)
            return True

        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error saving to CSV: %s", str(e))
            return False

    def load_from_json(self, filename: str = RESULTS_FILE) -> List[Dict[str, Any]]:
        """
        Load results from JSON file.

        Args:
            filename (str): Input filename

        Returns:
            List[Dict[str, Any]]: Loaded data
        """
        try:
            if not os.path.exists(filename):
                logger.warning("File %s does not exist", filename)
                return []

            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info("Successfully loaded %d records from %s", len(data), filename)
            return data

        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error loading from JSON: %s", str(e))
            return []
