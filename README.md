# 🎰 Casino AI Research Platform

## 🚀 Overview
Complete AI platform for testing strategies on casino games with **correct workflow**:

### ✅ CORRECT FLOW (As Required):
1. **FIRST**: Site selection (enter https:// URL)
2. **THEN**: Credentials (email, password)
3. **THEN**: Game selection (Blackjack, Roulette, etc.)
4. **THEN**: AI parameter configuration
5. **THEN**: Full auto-pilot with card counting
6. **SUPERVISION**: Assisted withdraw with user confirmation

## 🎯 Features Implemented

### 🤖 AI Capabilities
- ✅ **Card Counting** for Blackjack (Hi-Lo system)
- ✅ **Full Auto-Pilot** with configurable parameters
- ✅ **Bankroll Management** with stop-loss/stop-win
- ✅ **Basic Strategy** with count-based deviations
- ✅ **Reinforcement Learning** ready

### 🌐 Browser Automation
- ✅ **Login Automation** with credential management
- ✅ **Game State Detection** using computer vision
- ✅ **Action Execution** (bet, hit, stand, etc.)
- ✅ **Real-time Screenshot Capture**
- ✅ **Multi-site Support**

### 📊 Analysis & Monitoring
- ✅ **Monte Carlo Simulation**
- ✅ **Risk Analysis** (VaR, CVaR, Sharpe ratio)
- ✅ **Real-time Dashboard**
- ✅ **Session Logging**
- ✅ **Performance Metrics**

## 🎮 Supported Games

### Blackjack
- Hi-Lo Card Counting
- Basic Strategy
- Strategy Deviations
- Shoe Penetration Analysis

### Roulette
- Martingale System
- Fibonacci System
- D'Alembert System
- Pattern Recognition

### Baccarat
- Banker/Player Prediction
- Card Pattern Analysis
- Statistical Arbitrage

## 📋 Quick Start

### 1. Installation
```bash
# Clone repository
git clone https://github.com/yourusername/casino-ai-research.git
cd casino-ai-research

# Install dependencies
make setup
make install
```

### 2. Launch Web Interface (Recommended) 🌐
```bash
# Avvia l'interfaccia web - si apre automaticamente nel browser
python3 src/main.py
# Scegli opzione 1 (Web Interface)

# Oppure direttamente:
python3 run_web.py
```

L'interfaccia web si aprirà automaticamente su **http://localhost:8501**

### 3. Alternative: CLI Interface
```bash
# Run blackjack simulation
make simulate

# Or launch the CLI
python3 src/main.py
# Scegli opzione 2 (CLI Interface)
```

### 3. Web Dashboard
```bash
make dashboard
# Open http://localhost:8501
```

### 4. Run Tests
```bash
make test
```

## 🏗️ Project Structure

```
casino-ai-research/
├── src/                    # Source code
│   ├── ai/                # AI decision making
│   ├── automation/        # Browser automation
│   ├── environments/      # Game simulators
│   ├── ui/               # User interfaces
│   └── utils/            # Utilities
├── config/               # Configuration files
│   ├── sites/           # Site configurations
│   ├── games/           # Game rules
│   └── ai/              # AI parameters
├── notebooks/           # Jupyter notebooks
├── data/               # Simulation data
├── tests/              # Unit tests
└── docker/             # Containerization
```

## ⚙️ Configuration

### Site Configuration
Edit `config/sites/site_maker.yaml`:
```yaml
name: "Your Site"
url: "https://your-site.com"
login:
  email_selector: "input[name='email']"
  password_selector: "input[name='password']"
```

### AI Parameters
Edit `config/ai_config.yaml`:
```yaml
reinforcement_learning:
  algorithm: "PPO"
  learning_rate: 0.0003
  
bankroll_management:
  initial_bankroll: 10000
  risk_per_bet: 0.01
  stop_loss: 0.2
  stop_win: 0.3
```

## 🎲 AI Workflow Example

```python
from src.ai.decision_maker import AIDecisionMaker

# Configure AI
config = {
    "mode": "auto_pilot",
    "initial_bankroll": 10000,
    "risk_per_bet": 0.01,
    "stop_loss": 0.2,
    "stop_win": 0.3,
    "enable_card_counting": True
}

# Create AI instance
ai = AIDecisionMaker(config)

# Start auto-pilot session
ai.start_session()
```

## 📈 Performance Metrics

The AI tracks:
- **Win Rate**: Percentage of winning hands
- **Profit/Loss**: Bankroll evolution
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Maximum loss from peak
- **Card Count**: Running and true counts
- **Hands Played**: Session statistics

## 🔒 Security & Ethics

### Important Notes:
- **For Research Only**: This platform is for educational purposes
- **Site Ownership**: Only test on sites you own or have permission
- **Legal Compliance**: Follow all local gambling laws and regulations
- **Responsible Use**: Never use with money you cannot afford to lose

### Credential Security:
- Credentials are stored locally in encrypted format
- Never shared or transmitted
- Session-based with automatic cleanup

## 🐳 Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# Access services
# Dashboard: http://localhost:8501
# API: http://localhost:5000
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_blackjack.py -v

# Test with coverage
pytest --cov=src tests/
```

## 📚 Documentation

- Setup Guide
- API Reference
- Strategy Guide
- Troubleshooting

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Create Pull Request

## ⚠️ Disclaimer

This software is for educational and research purposes only.

- Gambling can be addictive
- Never risk money you cannot afford to lose
- Only use on sites you own or have explicit permission
- The authors assume no responsibility for misuse

## 📞 Support

For issues or questions:
- Check the documentation
- Open an issue
- Contact the development team

---

🎰 **Happy Researching!** 🤖

