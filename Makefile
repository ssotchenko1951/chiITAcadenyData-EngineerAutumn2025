.PHONY: help install test clean docker-up docker-down run-pipeline start-api migrate

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$\' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -e .

test: ## Run tests
	pytest tests/ -v

test-coverage: ## Run tests with coverage
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-e2e: ## Run end-to-end tests
	pytest tests/e2e/ -v

clean: ## Clean up generated files
	rm -rf data/processed/*
	rm -rf data/raw/*
	rm -rf reports/*
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -name "*.pyc" -delete

docker-up: ## Start Docker services
	docker-compose up -d

docker-down: ## Stop Docker services
	docker-compose down

docker-build: ## Build Docker images
	docker-compose build

run-pipeline: ## Run the data pipeline
	python -m src.main pipeline run

start-api: ## Start the FastAPI server
	python -m src.main api start

migrate: ## Run database migrations
	python -m src.main db migrate

setup-dev: ## Setup development environment
	mkdir -p data/raw data/processed reports logs
	cp .env.example .env
	make install-dev
	make migrate

lint: ## Run code linting
	flake8 src tests
	black --check src tests
	isort --check-only src tests

format: ## Format code
	black src tests
	isort src tests

prefect-start: ## Start Prefect server
	prefect server start

prefect-deploy: ## Deploy Prefect flow
	python src/infrastructure/orchestration/prefect_flow.py