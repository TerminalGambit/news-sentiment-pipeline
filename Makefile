.PHONY: install clean test run lint format help

# Python version
PYTHON := python3
PIP := pip3

# Project directories
SRC_DIR := src
DATA_DIR := data
TEST_DIR := tests

# Default target
.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies using pip3"
	@echo "  make clean      - Remove Python cache files and data directory"
	@echo "  make test       - Run tests"
	@echo "  make run        - Run the sentiment analysis pipeline"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code using black"
	@echo "  make help       - Show this help message"

install:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install feedparser beautifulsoup4 transformers torch pandas numpy python-dotenv requests tqdm
	$(PIP) install black pylint pytest pytest-cov

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -rf $(DATA_DIR)/*

test:
	@echo "Running tests..."
	$(PYTHON) -m pytest $(TEST_DIR) -v --cov=$(SRC_DIR)

run:
	@echo "Running sentiment analysis pipeline..."
	$(PYTHON) -m $(SRC_DIR).pipeline

lint:
	@echo "Running linting checks..."
	pylint $(SRC_DIR)

format:
	@echo "Formatting code..."
	black $(SRC_DIR)

# Create necessary directories
setup:
	@echo "Setting up project structure..."
	mkdir -p $(DATA_DIR)
	mkdir -p $(TEST_DIR)

# Development environment setup
dev: setup install
	@echo "Development environment setup complete"

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv venv
	@echo "Virtual environment created. Activate it with: source venv/bin/activate"

# Update dependencies
update:
	@echo "Updating dependencies..."
	$(PIP) install --upgrade feedparser beautifulsoup4 transformers torch pandas numpy python-dotenv requests tqdm
	$(PIP) install --upgrade black pylint pytest pytest-cov 