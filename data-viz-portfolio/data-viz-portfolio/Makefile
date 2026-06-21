# ── Data Visualization Portfolio — Makefile ───────────────────────────────────
.PHONY: help install install-dev build test lint format clean run-api

PYTHON  = python3
PIP     = pip
SRC     = src
TESTS   = tests

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""

install:  ## Install runtime dependencies
	$(PIP) install -r requirements.txt

install-dev:  ## Install all dependencies including dev tools
	$(PIP) install -r requirements-dev.txt

build:  ## Generate all 6 charts
	$(PYTHON) $(SRC)/build_all.py

test:  ## Run test suite
	$(PYTHON) -m pytest $(TESTS)/ -v --tb=short

test-cov:  ## Run tests with coverage report
	$(PYTHON) -m pytest $(TESTS)/ -v --cov=$(SRC) --cov-report=term-missing --cov-report=html

lint:  ## Run flake8 linter
	$(PYTHON) -m flake8 $(SRC)/ $(TESTS)/ --max-line-length=100

format:  ## Auto-format with black + isort
	$(PYTHON) -m black $(SRC)/ $(TESTS)/
	$(PYTHON) -m isort $(SRC)/ $(TESTS)/

run-api:  ## Start Flask API server on port 5000
	$(PYTHON) app.py

clean:  ## Remove generated files and caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -f coverage.xml .coverage
	@echo "Cleaned."

clean-charts:  ## Remove generated chart PNGs
	rm -f assets/images/*.png
	@echo "Charts removed."

all: install build test  ## Install + build + test (full pipeline)
