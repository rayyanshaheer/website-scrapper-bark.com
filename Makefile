.PHONY: help install test clean lint format setup demo

# Default target
help:
	@echo "Bark.com Contact Information Scraper - Makefile"
	@echo "================================================"
	@echo ""
	@echo "Available targets:"
	@echo "  setup     - Run the setup script and create virtual environment"
	@echo "  install   - Install dependencies in existing environment"
	@echo "  test      - Run the test suite"
	@echo "  lint      - Run code linting with flake8"
	@echo "  format    - Format code with black"
	@echo "  demo      - Run the production demo"
	@echo "  clean     - Clean up generated files and cache"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Quick start: make setup && make demo"

# Setup the entire project
setup:
	@echo "🚀 Setting up the project..."
	bash setup.sh

# Install dependencies only
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Run tests
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

# Run linting
lint:
	@echo "🔍 Running code linting..."
	flake8 src/ tests/ examples/ --max-line-length=88

# Format code
format:
	@echo "✨ Formatting code..."
	black src/ tests/ examples/

# Run demo
demo:
	@echo "🎯 Running production demo..."
	python examples/production_demo.py

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/
	@echo "✅ Cleanup complete"

# Quick scraping examples
example-cleaners:
	@echo "🧽 Scraping cleaners in London..."
	python src/scraper_cli.py cleaners --location london --max 10

example-gardeners:
	@echo "🌱 Scraping gardeners in Manchester..."
	python src/scraper_cli.py gardeners --location manchester --max 10

example-personal-trainers:
	@echo "💪 Scraping personal trainers in Birmingham..."
	python src/scraper_cli.py "personal trainers" --location birmingham --max 10
