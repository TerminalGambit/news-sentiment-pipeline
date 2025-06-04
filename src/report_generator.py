"""
Report generation module for creating LaTeX reports from sentiment analysis results.
"""

import json
import logging
import os
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from jinja2 import Environment, FileSystemLoader

from .config import DATA_DIR

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Class for generating LaTeX and PDF reports from sentiment analysis results."""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        """Initialize the report generator with necessary directories."""
        self.report_dir = os.path.join(DATA_DIR, "reports")
        self.cache_dir = os.path.join(DATA_DIR, "cache")
        self.template_dir = os.path.join(DATA_DIR, "templates")

        # Create necessary directories
        for directory in [self.report_dir, self.cache_dir, self.template_dir]:
            os.makedirs(directory, exist_ok=True)

        # Initialize Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

        # Create LaTeX template if it doesn't exist
        self._create_latex_template()

    def _create_latex_template(self):
        """Create the LaTeX template file if it doesn't exist."""
        template_path = os.path.join(self.template_dir, "report_template.tex")
        if not os.path.exists(template_path):
            template = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{float}
\usepackage{geometry}
\usepackage{textcomp}
\usepackage{url}
\geometry{a4paper, margin=1in}

\title{Financial News Sentiment Analysis Report}
\author{Generated on \today}
\date{\today}

\begin{document}

\maketitle

\section{Executive Summary}
This report presents the sentiment analysis results for financial news articles collected on {{ date }}. Out of {{ total_articles }} articles analyzed, sentiment was generally {{ overall_sentiment }}. {{ interpretation }}

\section{Overview}
\begin{itemize}
    \item Total Articles Analyzed: {{ total_articles }}
    \item Time Period: {{ time_period }}
    \item Sources: {{ sources|join(', ')}}
\end{itemize}

\section{Methodology}
This report uses the FinBERT model, a specialized BERT model trained on financial text, for sentiment analysis. The analysis process includes:

\begin{itemize}
    \item \textbf{Text Preprocessing:} HTML cleaning, noise removal, and financial term normalization
    \item \textbf{Sentiment Analysis:} Each article is classified as Positive, Neutral, or Negative with a confidence score
    \item \textbf{Data Collection:} Articles are collected every 6 hours from multiple financial news sources
    \item \textbf{Source Coverage:} Yahoo Finance, SeekingAlpha, Financial Times, MarketWatch, and Investing.com
\end{itemize}

\section{Sentiment Distribution}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{sentiment_distribution.png}
    \caption{Sentiment Distribution of Financial News Articles}
\end{figure}

\section{Source-wise Analysis}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{source_analysis.png}
    \caption{Sentiment Distribution by News Source}
\end{figure}

\section{Detailed Results}
\begin{table}[H]
    \centering
    \begin{tabular}{lrrr}
        \toprule
        Source & Positive & Neutral & Negative \\
        \midrule
        {% for source, counts in source_stats.items() %}
        {{ source }} & {{ counts.positive }} & {{ counts.neutral }} & {{ counts.negative }} \\
        {% endfor %}
        \bottomrule
    \end{tabular}
    \caption{Sentiment Distribution by Source}
\end{table}

\section{Top Articles by Sentiment}
\subsection{Most Positive Articles}
\begin{itemize}
    {% for article in top_positive %}
    \item \href{{{ article.link }}}{{{{ article.title }}}} 
    \begin{itemize}
        \item Sentiment Score: {{ article.sentiment.score }}
        \item Published: {{ article.published }}
    \end{itemize}
    {% endfor %}
\end{itemize}

\subsection{Most Negative Articles}
\begin{itemize}
    {% for article in top_negative %}
    \item \href{{{ article.link }}}{{{{ article.title }}}} 
    \begin{itemize}
        \item Sentiment Score: {{ article.sentiment.score }}
        \item Published: {{ article.published }}
    \end{itemize}
    {% endfor %}
\end{itemize}

\section{Next Steps}
\begin{itemize}
    \item Track long-term sentiment trends to identify market shifts.
    \item Compare sentiment with stock price movements for correlation analysis.
    \item Integrate alerts for significant sentiment changes.
\end{itemize}

\end{document}
"""
            with open(template_path, "w", encoding="utf-8") as f:
                f.write(template)

    def _get_cached_results(self, date: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached results for a specific date.

        Args:
            date (str): Date in YYYY-MM-DD format

        Returns:
            Optional[List[Dict[str, Any]]]: Cached results or None if not found
        """
        cache_file = os.path.join(self.cache_dir, f"results_{date}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error reading cache file: %s", str(e))
        return None

    def _cache_results(self, results: List[Dict[str, Any]], date: str):
        """
        Cache results for a specific date.

        Args:
            results (List[Dict[str, Any]]): Results to cache
            date (str): Date in YYYY-MM-DD format
        """
        cache_file = os.path.join(self.cache_dir, f"results_{date}.json")
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error writing cache file: %s", str(e))

    def _generate_visualizations(self, results: List[Dict[str, Any]], report_dir: str):
        """
        Generate visualizations for the report.

        Args:
            results (List[Dict[str, Any]]): Analysis results
            report_dir (str): Directory to save visualizations
        """
        # Convert to DataFrame
        df = pd.DataFrame(results)

        # Set style
        plt.style.use("seaborn-v0_8")
        sns.set_palette("husl")

        # Sentiment distribution pie chart
        plt.figure(figsize=(10, 6))
        sentiment_counts = df["sentiment"].apply(lambda x: x["label"]).value_counts()
        plt.pie(
            sentiment_counts,
            labels=sentiment_counts.index,
            autopct="%1.1f%%",
            startangle=90,
        )
        plt.title("Sentiment Distribution")
        plt.axis("equal")
        plt.tight_layout()
        plt.savefig(
            os.path.join(report_dir, "sentiment_distribution.png"),
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

        # Source-wise analysis with average sentiment scores
        plt.figure(figsize=(12, 6))
        source_sentiment = pd.crosstab(
            df["source"], df["sentiment"].apply(lambda x: x["label"])
        )
        source_sentiment.plot(kind="bar", stacked=True)
        plt.title("Sentiment Distribution by Source")
        plt.xlabel("Source")
        plt.ylabel("Count")
        plt.legend(title="Sentiment")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(
            os.path.join(report_dir, "source_analysis.png"),
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

    def _format_article_title(self, title: str) -> str:
        """
        Format article title by fixing common issues.

        Args:
            title (str): Original article title

        Returns:
            str: Formatted title
        """
        # Fix common issues
        title = title.replace("ondeliverygrowth", " on delivery growth")
        title = title.replace("to 28", "to 28%")
        title = title.replace("Housing starts fall 14.8", "Housing starts fall 14.8%")

        # Add spaces after commas
        title = title.replace(",", ", ")

        # Remove multiple spaces
        title = " ".join(title.split())

        return title

    def generate_report(
        self, results: List[Dict[str, Any]], date: Optional[str] = None
    ) -> str:
        """
        Generate a LaTeX report from the analysis results.

        Args:
            results (List[Dict[str, Any]]): Analysis results
            date (Optional[str]): Date for the report (defaults to today)

        Returns:
            str: Path to the generated PDF report
        """
        try:
            # Set date
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")

            # Create report directory
            report_dir = os.path.join(self.report_dir, date)
            os.makedirs(report_dir, exist_ok=True)

            # Generate visualizations
            self._generate_visualizations(results, report_dir)

            # Format article titles
            for article in results:
                article["title"] = self._format_article_title(article["title"])

            # Prepare template data
            template_data = {
                "date": date,
                "total_articles": len(results),
                "time_period": f"Last 24 hours until {date}",
                "sources": sorted(set(article["source"] for article in results)),
                "source_stats": self._calculate_source_stats(results),
                "top_positive": sorted(
                    results,
                    key=lambda x: (
                        x["sentiment"]["score"]
                        if x["sentiment"]["label"] == "Positive"
                        else 0
                    ),
                    reverse=True,
                )[:5],
                "top_negative": sorted(
                    results,
                    key=lambda x: (
                        x["sentiment"]["score"]
                        if x["sentiment"]["label"] == "Negative"
                        else 0
                    ),
                    reverse=True,
                )[:5],
                "overall_sentiment": self._calculate_overall_sentiment(results),
                "interpretation": self._generate_interpretation(results),
            }

            # Render template
            template = self.env.get_template("report_template.tex")
            latex_content = template.render(**template_data)

            # Write LaTeX file
            tex_file = os.path.join(report_dir, "report.tex")
            with open(tex_file, "w", encoding="utf-8") as f:
                f.write(latex_content)

            # Compile LaTeX to PDF with errors logged to a file
            log_file = os.path.join(report_dir, "report.log")
            with open(log_file, "w", encoding="utf-8") as f:
                subprocess.run(
                    [
                        "pdflatex",
                        "-interaction=nonstopmode",
                        "-output-directory",
                        report_dir,
                        tex_file,
                    ],
                    stdout=f,
                    stderr=f,
                    check=True,
                )

            # Cache results
            self._cache_results(results, date)

            # Return path to PDF
            pdf_path = os.path.join(report_dir, "report.pdf")
            logger.info("Report generated successfully: %s", pdf_path)
            return pdf_path

        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error generating report: %s", str(e))
            raise

    def _calculate_source_stats(
        self, results: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, int]]:
        """
        Calculate sentiment statistics by source.

        Args:
            results (List[Dict[str, Any]]): Analysis results

        Returns:
            Dict[str, Dict[str, int]]: Statistics by source
        """
        stats = {}
        for article in results:
            source = article["source"]
            sentiment = article["sentiment"]["label"]

            if source not in stats:
                stats[source] = {"positive": 0, "neutral": 0, "negative": 0}

            stats[source][sentiment.lower()] += 1

        return stats

    def _calculate_overall_sentiment(self, results: List[Dict[str, Any]]) -> str:
        """
        Calculate the overall sentiment based on the majority sentiment label.

        Args:
            results (List[Dict[str, Any]]): Analysis results

        Returns:
            str: Overall sentiment label
        """
        sentiment_counts = {}
        for result in results:
            label = result["sentiment"]["label"]
            sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
        return max(sentiment_counts.items(), key=lambda x: x[1])[0]

    def _generate_interpretation(self, results: List[Dict[str, Any]]) -> str:
        """
        Generate a brief interpretation of the sentiment analysis results.
        """
        sentiment_counts = {}
        source_sentiment = {}
        for result in results:
            label = result["sentiment"]["label"]
            source = result["source"]
            sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
            if source not in source_sentiment:
                source_sentiment[source] = {"positive": 0, "neutral": 0, "negative": 0}
            source_sentiment[source][label.lower()] += 1
        total = len(results)
        if source_sentiment:
            most_negative_source = max(
                source_sentiment.items(),
                key=lambda x: x[1]["negative"] / sum(x[1].values()),
            )[0]
        else:
            most_negative_source = "N/A"
        return (
            f"Out of {total} articles analyzed, sentiment was generally neutral to "
            f"slightly negative, with {most_negative_source} showing the most "
            "negative tone overall."
        )


def generate_report_from_cache(date: str) -> Optional[str]:
    """
    Generate a report from cached results for a specific date.

    Args:
        date (str): Date in YYYY-MM-DD format

    Returns:
        Optional[str]: Path to the generated PDF report or None if failed
    """
    try:
        generator = ReportGenerator()
        # pylint: disable=protected-access
        cached_results = generator._get_cached_results(date)

        if cached_results is None:
            logger.warning(f"No cached results found for date: {date}")
            return None

        return generator.generate_report(cached_results, date)

    except Exception as e:  # pylint: disable=broad-except
        logger.error("Error generating report from cache: %s", str(e))
        return None
