# Makefile for Everything Tracker Backend

.PHONY: help install dev test test-local test-aws db-start db-stop db-setup clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

dev: ## Run development server
	uv run fastapi dev --port 8080

test: ## Run all tests
	uv run python -m pytest

db-start: ## Start local DynamoDB container
	docker-compose up -d dynamodb-local

db-stop: ## Stop local DynamoDB container
	docker-compose down

db-setup: ## Set up local DynamoDB tables
	uv run python scripts/setup_local_db.py

db-init: db-start db-setup ## Start DynamoDB and set up tables

clean: ## Clean up containers and volumes
	docker-compose down -v