import pytest
from src.ai.decision_maker import AIDecisionMaker

def test_ai_initialization():
    """Test AI initialization"""
    config = {
        "mode": "auto_pilot",
        "initial_bankroll": 10000,
        "enable_card_counting": True
    }
    
    ai = AIDecisionMaker(config)
    assert ai.initial_bankroll == 10000
    assert ai.config["mode"] == "auto_pilot"

def test_card_counting():
    """Test card counting logic"""
    config = {
        "enable_card_counting": True,
        "decks_remaining": 6
    }
    
    ai = AIDecisionMaker(config)
    assert ai.card_count == 0
    assert ai.true_count == 0.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

