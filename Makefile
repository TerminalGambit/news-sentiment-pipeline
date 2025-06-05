# Variables
PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip
FLASK = $(VENV)/bin/flask
NODE = node
NPM = npm

# Macro commands
.PHONY: all clean install test run build docker-build docker-run

all: install build

clean:
	@echo "Cleaning up..."
	rm -rf backend/$(VENV)
	rm -rf frontend/node_modules
	rm -rf backend/__pycache__
	rm -rf backend/*/__pycache__
	rm -rf backend/*/*/__pycache__
	rm -rf backend/logs/*
	rm -rf backend/data/*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

install: install-backend install-frontend

test: test-backend test-frontend

run: run-backend run-frontend

build: build-backend build-frontend

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-run:
	@echo "Starting Docker containers..."
	docker-compose up -d

# Micro commands for backend
.PHONY: install-backend test-backend run-backend build-backend

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && \
	$(PYTHON) -m venv $(VENV) && \
	. $(VENV)/bin/activate && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r requirements.txt

test-backend:
	@echo "Running backend tests..."
	cd backend && \
	. $(VENV)/bin/activate && \
	pytest

run-backend:
	@echo "Starting backend server..."
	cd backend && \
	. $(VENV)/bin/activate && \
	$(FLASK) run

build-backend:
	@echo "Building backend..."
	cd backend && \
	. $(VENV)/bin/activate && \
	$(PIP) install -r requirements.txt

# Micro commands for frontend
.PHONY: install-frontend test-frontend run-frontend build-frontend

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && \
	$(NPM) install

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && \
	$(NPM) test

run-frontend:
	@echo "Starting frontend development server..."
	cd frontend && \
	$(NPM) start

build-frontend:
	@echo "Building frontend..."
	cd frontend && \
	$(NPM) run build

# Development commands
.PHONY: dev-backend dev-frontend dev

dev-backend:
	@echo "Starting backend in development mode..."
	cd backend && \
	. $(VENV)/bin/activate && \
	$(FLASK) run --debug

dev-frontend:
	@echo "Starting frontend in development mode..."
	cd frontend && \
	$(NPM) start

dev: dev-backend dev-frontend

# Docker commands
.PHONY: docker-clean docker-logs docker-stop

docker-clean:
	@echo "Cleaning up Docker containers and images..."
	docker-compose down -v
	docker system prune -f

docker-logs:
	@echo "Showing Docker logs..."
	docker-compose logs -f

docker-stop:
	@echo "Stopping Docker containers..."
	docker-compose down

# Help command
.PHONY: help

help:
	@echo "Available commands:"
	@echo "  all            - Install dependencies and build the application"
	@echo "  clean          - Clean up all generated files and caches"
	@echo "  install        - Install all dependencies"
	@echo "  test           - Run all tests"
	@echo "  run            - Run the application"
	@echo "  build          - Build the application"
	@echo "  docker-build   - Build Docker images"
	@echo "  docker-run     - Run Docker containers"
	@echo "  dev            - Run in development mode"
	@echo "  docker-clean   - Clean up Docker resources"
	@echo "  docker-logs    - Show Docker logs"
	@echo "  docker-stop    - Stop Docker containers"
	@echo "  help           - Show this help message" 