#!/bin/bash
echo "🎰 Casino AI Research Platform - Setup Script"
echo "=============================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python not found. Install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Create virtual environment
echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo -e "${RED}❌ Could not activate virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${YELLOW}⬆️ Upgrading pip...${NC}"
pip install --upgrade pip
echo -e "${GREEN}✅ Pip upgraded${NC}"

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi

# Install Playwright
echo -e "${YELLOW}🌐 Installing Playwright...${NC}"
if command -v playwright &>/dev/null; then
    echo -e "${GREEN}✅ Playwright already installed${NC}"
else
    pip install playwright
    echo -e "${GREEN}✅ Playwright installed${NC}"
fi

echo -e "${YELLOW}🔧 Installing Chromium browser...${NC}"
playwright install chromium
playwright install-deps
echo -e "${GREEN}✅ Chromium browser installed${NC}"

# Create data directories
echo -e "${YELLOW}📁 Creating data directories...${NC}"
mkdir -p data/simulations data/live_sessions data/training_data data/logs
mkdir -p notebooks/results
echo -e "${GREEN}✅ Data directories created${NC}"

# Test installation
echo -e "${YELLOW}🧪 Testing installation...${NC}"
python -c "import numpy; print('✅ numpy:', numpy.__version__)" 2>/dev/null || echo "⚠️  numpy not installed"
python -c "import pandas; print('✅ pandas:', pandas.__version__)" 2>/dev/null || echo "⚠️  pandas not installed"
python -c "import playwright; print('✅ playwright: OK')" 2>/dev/null || echo "⚠️  playwright not installed"

echo ""
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Configure your site in config/sites/site_maker.yaml"
echo "2. Run: python src/main.py"
echo "3. Or launch dashboard: make dashboard"
echo ""
echo -e "${GREEN}Happy researching! 🎰🤖${NC}"

