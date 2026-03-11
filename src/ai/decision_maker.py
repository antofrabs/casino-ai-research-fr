#!/usr/bin/env python3
"""
🤖 AIDecisionMaker - AI in auto-pilota con conteggio carte
===============================================================

Caratteristiche:
1. Auto-pilota completo
2. Conteggio carte per Blackjack
3. Gestione bankroll intelligente
4. Stop-loss/stop-win automatici
5. Withdraw assistito
"""
import time
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class GameAction(Enum):
    """Azioni disponibili nei giochi"""
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"
    SURRENDER = "surrender"
    INSURANCE = "insurance"

@dataclass
class GameState:
    """Stato corrente del gioco"""
    player_hand: List[str]
    dealer_upcard: str
    player_value: int
    dealer_value: int
    available_actions: List[GameAction]
    true_count: float = 0.0
    bankroll: float = 0.0
    current_bet: float = 0.0

class AIDecisionMaker:
    """AI che gioca in auto-pilota con parametri configurabili"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.is_running = False
        
        # Sistema di conteggio carte
        self.card_count = 0
        self.true_count = 0.0
        self.decks_remaining = config.get("decks_remaining", 6)
        
        # Bankroll management
        self.initial_bankroll = config.get("initial_bankroll", 10000)
        self.current_bankroll = self.initial_bankroll
        self.session_profit = 0.0
        
        # Statistiche
        self.hands_played = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        
        # Strategie
        self.basic_strategy = self.load_basic_strategy()
        self.counting_system = config.get("counting_system", "hi_lo")
    
    def load_basic_strategy(self) -> Dict:
        """Carica la strategia base per Blackjack"""
        # Strategia semplificata
        return {
            # (player_value, dealer_upcard): action
            (12, 2): GameAction.HIT,
            (12, 3): GameAction.HIT,
            (12, 4): GameAction.STAND,
            (12, 5): GameAction.STAND,
            (12, 6): GameAction.STAND,
            # ... altre regole
        }
    
    def start_session(self):
        """Avvia sessione in auto-pilota"""
        print("🤖 AI Session Started")
        print(f"   Mode: {self.config.get('mode', 'auto_pilot')}")
        print(f"   Bankroll: ${self.current_bankroll}")
        print(f"   Card Counting: {self.config.get('enable_card_counting', False)}")
        
        self.is_running = True
        self.session_start_time = time.time()
        
        # Avvia loop principale
        self.main_loop()
    
    def main_loop(self):
        """Loop principale dell'AI"""
        max_hands = self.config.get("max_hands", 1000)
        
        while self.is_running and self.hands_played < max_hands:
            # Controlla condizioni di stop
            if self.check_stop_conditions():
                print("🛑 Stop condition reached")
                break
            
            # Gioca una mano
            self.play_hand()
            self.hands_played += 1
            
            # Log progresso
            if self.hands_played % 100 == 0:
                self.log_progress()
            
            # Simula tempo tra le mani
            time.sleep(0.05)
        
        # Fine sessione
        self.end_session()
    
    def play_hand(self):
        """Gioca una singola mano"""
        # 1. Calcola puntata in base al true count
        bet_amount = self.calculate_bet()
        
        # 2. Pesca carte iniziali
        player_hand = self.deal_hand()
        dealer_upcard = self.deal_card()
        
        # 3. Crea stato gioco
        game_state = GameState(
            player_hand=player_hand,
            dealer_upcard=dealer_upcard,
            player_value=self.calculate_hand_value(player_hand),
            dealer_value=self.calculate_hand_value([dealer_upcard]),
            available_actions=self.get_available_actions(player_hand),
            true_count=self.true_count,
            bankroll=self.current_bankroll,
            current_bet=bet_amount
        )
        
        # 4. Decisione AI
        action = self.make_decision(game_state)
        
        # 5. Risolvi mano
        outcome = self.resolve_hand(game_state, action)
        
        # 6. Aggiorna bankroll
        self.update_bankroll(outcome, bet_amount)
        
        # 7. Aggiorna conteggio carte
        if self.config.get("enable_card_counting", False):
            self.update_card_count(player_hand + [dealer_upcard])
    
    def calculate_bet(self) -> float:
        """Calcola la puntata in base al true count"""
        base_bet = self.current_bankroll * self.config.get("risk_per_bet", 0.01)
        
        if self.config.get("enable_card_counting", False):
            # Aumenta puntata con true count positivo
            if self.true_count >= 2:
                multiplier = 1 + (self.true_count / 2)
                base_bet *= min(multiplier, 10)  # Max 10x
            
            # Riduci puntata con true count negativo
            elif self.true_count <= -1:
                base_bet *= 0.5
        
        # Limiti
        min_bet = self.config.get("min_bet", 10)
        max_bet = self.current_bankroll * 0.05  # Max 5% del bankroll
        
        return max(min_bet, min(base_bet, max_bet))
    
    def update_card_count(self, cards: List[str]):
        """Aggiorna il conteggio carte (sistema Hi-Lo)"""
        for card in cards:
            if card in ['2', '3', '4', '5', '6']:
                self.card_count += 1
            elif card in ['10', 'J', 'Q', 'K', 'A']:
                self.card_count -= 1
        
        # Calcola true count
        if self.decks_remaining > 0:
            self.true_count = self.card_count / self.decks_remaining
    
    def make_decision(self, game_state: GameState) -> GameAction:
        """Prende decisione in base a strategia base + deviazioni per conteggio"""
        # Prima controlla deviazioni per conteggio
        deviation = self.get_count_deviation(game_state)
        if deviation:
            return deviation
        
        # Altrimenti usa strategia base
        key = (game_state.player_value, game_state.dealer_upcard)
        return self.basic_strategy.get(key, GameAction.STAND)
    
    def get_count_deviation(self, game_state: GameState) -> Optional[GameAction]:
        """Deviazioni in base al true count"""
        if not self.config.get("enable_card_counting", False):
            return None
        
        true_count = game_state.true_count
        
        # Deviazioni standard
        if game_state.player_value == 16 and game_state.dealer_upcard in ['9', '10', 'A']:
            if true_count >= 0:
                return GameAction.STAND
            else:
                return GameAction.HIT
        
        if game_state.player_value == 15 and game_state.dealer_upcard == '10':
            if true_count >= 4:
                return GameAction.STAND
            else:
                return GameAction.HIT
        
        return None
    
    def check_stop_conditions(self) -> bool:
        """Controlla se fermare la sessione"""
        session_profit = self.current_bankroll - self.initial_bankroll
        profit_pct = (session_profit / self.initial_bankroll) * 100
        
        # Stop-loss
        stop_loss = self.config.get("stop_loss", 0.2) * 100  # Convert to percentage
        if profit_pct <= -stop_loss:
            print(f"📉 Stop-loss reached: {profit_pct:.1f}%")
            return True
        
        # Stop-win
        stop_win = self.config.get("stop_win", 0.3) * 100  # Convert to percentage
        if profit_pct >= stop_win:
            print(f"📈 Stop-win reached: {profit_pct:.1f}%")
            return True
        
        return False
    
    def log_progress(self):
        """Logga progresso sessione"""
        session_profit = self.current_bankroll - self.initial_bankroll
        profit_pct = (session_profit / self.initial_bankroll) * 100
        
        print(f"📊 Hands: {self.hands_played} | "
              f"Bankroll: ${self.current_bankroll:.0f} ({profit_pct:+.1f}%) | "
              f"Count: {self.card_count} ({self.true_count:+.1f})")
    
    def end_session(self):
        """Termina la sessione"""
        self.is_running = False
        session_duration = time.time() - self.session_start_time
        
        print("\n" + "=" * 50)
        print("🤖 AI Session Completed")
        print("=" * 50)
        print(f"🎲 Hands played: {self.hands_played}")
        print(f"💰 Initial bankroll: ${self.initial_bankroll:.2f}")
        print(f"💰 Final bankroll: ${self.current_bankroll:.2f}")
        print(f"📈 Profit: ${self.current_bankroll - self.initial_bankroll:+.2f}")
        print(f"📊 Win rate: {(self.wins / self.hands_played * 100 if self.hands_played > 0 else 0):.1f}%")
        print(f"⏱️  Duration: {session_duration:.1f} seconds")
        print(f"🎴 Final count: {self.card_count} (True: {self.true_count:.2f})")
    
    # Metodi di supporto (simulati)
    def deal_hand(self) -> List[str]:
        """Pesca una mano"""
        return [self.deal_card(), self.deal_card()]
    
    def deal_card(self) -> str:
        """Pesca una carta"""
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return random.choice(cards)
    
    def calculate_hand_value(self, hand: List[str]) -> int:
        """Calcola valore mano Blackjack"""
        value = 0
        aces = 0
        
        for card in hand:
            if card in ['J', 'Q', 'K']:
                value += 10
            elif card == 'A':
                value += 11
                aces += 1
            else:
                value += int(card)
        
        # Adjust aces if bust
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def get_available_actions(self, hand: List[str]) -> List[GameAction]:
        """Restituisce azioni disponibili"""
        actions = [GameAction.HIT, GameAction.STAND]
        
        if len(hand) == 2:
            actions.extend([GameAction.DOUBLE, GameAction.SURRENDER])
            
            if hand[0] == hand[1]:
                actions.append(GameAction.SPLIT)
        
        return actions
    
    def resolve_hand(self, game_state: GameState, action: GameAction) -> str:
        """Risolve il risultato della mano"""
        # Simula risultato
        outcomes = ['win', 'loss', 'push']
        weights = [0.48, 0.47, 0.05]
        
        # Ajust weights based on true count
        if self.config.get("enable_card_counting", False):
            if self.true_count > 0:
                weights = [0.50 + (self.true_count * 0.01), 
                          0.45 - (self.true_count * 0.01), 
                          0.05]
            elif self.true_count < 0:
                weights = [0.46 + (self.true_count * 0.01), 
                          0.49 - (self.true_count * 0.01), 
                          0.05]
        
        return random.choices(outcomes, weights=weights)[0]
    
    def update_bankroll(self, outcome: str, bet: float):
        """Aggiorna bankroll in base al risultato"""
        if outcome == 'win':
            self.current_bankroll += bet
            self.wins += 1
        elif outcome == 'loss':
            self.current_bankroll -= bet
            self.losses += 1
        else:  # push
            self.pushes += 1

# Esempio di utilizzo
if __name__ == "__main__":
    config = {
        "mode": "auto_pilot",
        "initial_bankroll": 10000,
        "risk_per_bet": 0.01,
        "stop_loss": 0.2,
        "stop_win": 0.3,
        "enable_card_counting": True,
        "max_hands": 100,
        "counting_system": "hi_lo",
        "decks_remaining": 6
    }
    
    ai = AIDecisionMaker(config)
    ai.start_session()

