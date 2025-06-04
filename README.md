# Financial News Sentiment Analysis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/TerminalGambit/news-sentiment-pipeline/actions/workflows/tests.yml/badge.svg)](https://github.com/TerminalGambit/news-sentiment-pipeline/actions/workflows/tests.yml)
[![Lint](https://github.com/TerminalGambit/news-sentiment-pipeline/actions/workflows/lint.yml/badge.svg)](https://github.com/TerminalGambit/news-sentiment-pipeline/actions/workflows/lint.yml)

A Python package for analyzing sentiment in financial news articles using FinBERT.

## Features

- Fetches financial news from multiple RSS feeds (Yahoo Finance, CNBC, Reuters)
- Cleans and preprocesses article text
- Performs sentiment analysis using FinBERT
- Saves results in both JSON and CSV formats
- Comprehensive logging and error handling
- Modular and extensible design

## Quick Start

```bash
# Clone the repository
git clone https://github.com/TerminalGambit/news-sentiment-pipeline.git
cd news-sentiment-pipeline

# Install dependencies
make install

# Run the pipeline
make run
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/TerminalGambit/news-sentiment-pipeline.git
cd news-sentiment-pipeline
```

2. Install dependencies using Make:

```bash
make install
```

Or for a complete development setup:

```bash
make dev
```

## Available Make Commands

- `make install` - Install dependencies using pip3
- `make clean` - Remove Python cache files and data directory
- `make test` - Run tests
- `make run` - Run the sentiment analysis pipeline
- `make lint` - Run linting checks
- `make format` - Format code using black
- `make help` - Show all available commands
- `make setup` - Create necessary directories
- `make dev` - Setup development environment
- `make venv` - Create virtual environment
- `make update` - Update dependencies to latest versions

## Usage

### Basic Usage

```python
from src.pipeline import SentimentAnalysisPipeline

# Initialize and run the pipeline
pipeline = SentimentAnalysisPipeline()
results = pipeline.run()
```

Or simply use:

```bash
make run
```

### Custom Usage

```python
from src.news_ingestion import fetch_all_feeds
from src.text_processor import process_article
from src.sentiment_analyzer import SentimentAnalyzer
from src.storage import DataStorage

# Fetch articles
articles = fetch_all_feeds()

# Process articles
processed_articles = []
for article in articles:
    processed = process_article(article)
    if processed:
        processed_articles.append(processed)

# Analyze sentiment
analyzer = SentimentAnalyzer()
results = analyzer.analyze_articles(processed_articles)

# Save results
storage = DataStorage()
storage.save_to_json(results)
storage.save_to_csv(results)
```

## Output Format

The pipeline generates two types of output files:

1. JSON file (`data/sentiment_results.json`):

```json
[
  {
    "title": "Article Title",
    "summary": "Article Summary",
    "link": "Article URL",
    "published": "Publication Date",
    "source": "Source URL",
    "timestamp": "Processing Timestamp",
    "processed_text": "Cleaned Text",
    "sentiment": {
      "label": "Positive/Negative/Neutral",
      "score": 0.95
    }
  }
]
```

2. CSV file (`data/sentiment_results_YYYYMMDD_HHMMSS.csv`):
   - Contains flattened data with sentiment label and score in separate columns
   - Includes all article metadata
   - Timestamp in filename for historical tracking

## Configuration

Configuration settings can be modified in `src/config.py`:

- RSS feed URLs
- Model settings
- File paths
- Text preprocessing parameters

## Development

### Code Quality

The project uses several tools to maintain code quality:

- `black` for code formatting
- `pylint` for code linting
- `pytest` for testing
- `pytest-cov` for test coverage

Run these tools using make commands:

```bash
make format  # Format code
make lint    # Run linting
make test    # Run tests
```

### Updating Dependencies

To update all dependencies to their latest versions:

```bash
make update
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
