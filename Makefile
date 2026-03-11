# 🎰 Casino AI Research Platform - Makefile
# ===============================================================

.PHONY: help setup install test simulate train dashboard clean

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

help:
	@echo "$(YELLOW)🎰 Casino AI Research Platform$(NC)"
	@echo ""
	@echo "$(GREEN)Available commands:$(NC)"
	@echo "  make setup        - Install all dependencies"
	@echo "  make install      - Install Playwright browser"
	@echo "  make test         - Run all tests"
	@echo "  make simulate     - Run blackjack simulation"
	@echo "  make train        - Train AI models"
	@echo "  make dashboard    - Launch web dashboard"
	@echo "  make api          - Start REST API server"
	@echo "  make clean        - Clean project"
	@echo "  make lint         - Run code linters"
	@echo "  make format       - Format code"

setup:
	@echo "$(GREEN)📦 Installing Python dependencies...$(NC)"
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

install:
	@echo "$(GREEN)🌐 Installing Playwright browser...$(NC)"
	playwright install chromium
	playwright install-deps
	@echo "$(GREEN)✅ Browser installed$(NC)"

test:
	@echo "$(GREEN)🧪 Running tests...$(NC)"
	python -m pytest tests/ -v
	@echo "$(GREEN)✅ Tests completed$(NC)"

simulate:
	@echo "$(GREEN)🎲 Running blackjack simulation...$(NC)"
	python src/main.py
	@echo "$(GREEN)✅ Simulation completed$(NC)"

train:
	@echo "$(GREEN)🤖 Training AI models...$(NC)"
	python src/ai/train.py --epochs 100
	@echo "$(GREEN)✅ Training completed$(NC)"

dashboard:
	@echo "$(GREEN)📊 Launching dashboard...$(NC)"
	@echo "$(YELLOW)Dashboard available at: http://localhost:8501$(NC)"
	streamlit run src/dashboard/app.py

api:
	@echo "$(GREEN)🚀 Starting API server...$(NC)"
	@echo "$(YELLOW)API available at: http://localhost:8000$(NC)"
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

clean:
	@echo "$(GREEN)🧹 Cleaning project...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf data/simulations/temp_*
	rm -rf data/training_data/checkpoints/temp_*
	@echo "$(GREEN)✅ Project cleaned$(NC)"

lint:
	@echo "$(GREEN)🔍 Running linters...$(NC)"
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/

format:
	@echo "$(GREEN)✨ Formatting code...$(NC)"
	black src/ tests/
	isort src/ tests/

# Quick commands
run:
	@python src/main.py

notebook:
	@jupyter notebook notebooks/

.PHONY: all
all: setup install test
	@echo "$(GREEN)🎉 Setup complete! Ready to go.$(NC)"

