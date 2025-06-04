.PHONY: install clean test run lint format help report report-cache setup-latex web web-install finbert

# Python version
PYTHON := ./venv/bin/python3.10
PIP := ./venv/bin/pip3.10

# Project directories
SRC_DIR := src
DATA_DIR := data
TEST_DIR := tests
SCRIPTS_DIR := scripts

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
	@echo "  make report     - Generate report from latest analysis"
	@echo "  make report-cache DATE=YYYY-MM-DD - Generate report from cached data"
	@echo "  make setup-latex - Check and install required LaTeX packages"
	@echo "  make help       - Show this help message"
	@echo "  make web-install - Install web dependencies"
	@echo "  make web        - Start web interface"
	@echo "  make finbert    - Run the FinBERT playground web app"

install:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install feedparser beautifulsoup4 transformers torch pandas numpy python-dotenv requests tqdm
	$(PIP) install black pylint pytest pytest-cov
	$(PIP) install jinja2 matplotlib seaborn

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
	$(PIP) install isort
	isort $(SRC_DIR)
	black $(SRC_DIR)
	pylint $(SRC_DIR)

format:
	@echo "Formatting code..."
	black $(SRC_DIR)

# Create necessary directories
setup:
	@echo "Setting up project structure..."
	mkdir -p $(DATA_DIR)
	mkdir -p $(TEST_DIR)
	mkdir -p $(SCRIPTS_DIR)

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
	$(PIP) install --upgrade jinja2 matplotlib seaborn

# Report generation
report:
	@echo "Generating report from latest analysis..."
	$(PYTHON) -c "from src.report_generator import ReportGenerator; from src.storage import DataStorage; storage = DataStorage(); results = storage.load_from_json(); generator = ReportGenerator(); path = generator.generate_report(results); print(path)" > .last_report_path.tmp
	REPORT_PATH=$$(tail -n 1 .last_report_path.tmp | grep -o 'data/reports/[^ ]*report.pdf' || true); \
	if [ -z "$$REPORT_PATH" ]; then \
		echo "[ERROR] Report PDF path not found. Check logs for errors."; \
		exit 1; \
	else \
		echo "Opening report: $$REPORT_PATH"; \
		open "$$REPORT_PATH"; \
	fi

report-cache:
	@if [ -z "$(DATE)" ]; then \
		echo "Error: DATE parameter is required. Usage: make report-cache DATE=YYYY-MM-DD"; \
		exit 1; \
	fi
	@echo "Generating report from cached data for $(DATE)..."
	$(PYTHON) -c "from src.report_generator import generate_report_from_cache; generate_report_from_cache('$(DATE)')"

# LaTeX setup
setup-latex:
	@echo "Checking and installing LaTeX packages..."
	$(PYTHON) $(SCRIPTS_DIR)/check_latex.py

web-install:
	@echo "Installing web dependencies..."
	$(PIP) install flask

web:
	@echo "Starting web interface..."
	$(PYTHON) -c "from src.web_app import run_web_app; run_web_app()"

finbert:
	$(PYTHON) -m src.finbert_playground

prelint:
	@echo "Running prelint checks..."
	isort $(SRC_DIR)
	black $(SRC_DIR)
	black --check $(SRC_DIR)
	isort --check-only $(SRC_DIR)
	pylint $(SRC_DIR) 