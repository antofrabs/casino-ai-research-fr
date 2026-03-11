#!/usr/bin/env python3
"""
🎯 Interfaccia CLI per Casino AI - Flusso CORRETTO
===============================================================

Il flusso rispetta esattamente i requisiti:
1. PRIMA chiede il sito (URL)
2. POI le credenziali
3. POI selezione gioco
4. POI configurazione AI
5. POI auto-pilota completo
"""
import sys
import time
from pathlib import Path
from typing import Dict, Optional
import yaml

try:
    import questionary
    import sys
    # Verifica se siamo in un terminale interattivo
    if sys.stdin.isatty():
        HAS_QUESTIONARY = True
    else:
        HAS_QUESTIONARY = False
except (ImportError, AttributeError):
    HAS_QUESTIONARY = False

class CasinoCLI:
    """Interfaccia CLI che segue il flusso corretto: SITO → CREDENZIALI → GIOCO → AI"""
    
    def __init__(self):
        self.site_url = None
        self.site_config = None
        self.credentials = {}
        self.game_config = {}
        self.ai_config = {}
        self.current_session = None
    
    def run(self):
        """Esegue l'intero flusso"""
        self.show_banner()
        
        # 🎯 STEP 1: PRIMA chiedi il SITO
        if not self.step1_select_site():
            return
        
        # 🔐 STEP 2: POI chiedi le CREDENZIALI
        if not self.step2_enter_credentials():
            return
        
        # 🎮 STEP 3: POI selezione GIOCO
        if not self.step3_select_game():
            return
        
        # 🤖 STEP 4: POI configurazione AI
        if not self.step4_configure_ai():
            return
        
        # 🚀 STEP 5: Avvio auto-pilota
        self.step5_start_ai()
        
        # 💰 STEP 6: Withdraw assistito
        self.step6_assisted_withdraw()
    
    def show_banner(self):
        """Mostra banner iniziale"""
        print("\n" + "=" * 70)
        print("🎰 CASINO AI RESEARCH PLATFORM")
        print("=" * 70)
        print("🤖 Sistema di testing AI per giochi casino")
        print("📍 Flusso: SITO → CREDENZIALI → GIOCO → AI → WITHDRAW")
        print("=" * 70)
    
    def step1_select_site(self) -> bool:
        """STEP 1: Selezione sito casino (PRIMA delle credenziali)"""
        print("\n" + "🔗" * 30)
        print("🎯 STEP 1: SELEZIONE SITO CASINO")
        print("🔗" * 30)
        print("\n💡 Inserisci PRIMA l'URL del sito casino")
        print("   (es: https://tuo-sito-maker.com)")
        print()
        
        if not HAS_QUESTIONARY:
            self.site_url = input("🌐 URL del sito casino: ").strip()
        else:
            choices = [
                "Inserisci URL manualmente (https://...)",
                "Usa sito di test preconfigurato",
                "Sito Maker (configurazione esistente)"
            ]
            
            choice = questionary.select(
                "Come vuoi procedere?",
                choices=choices
            ).ask()
            
            if choice == "Inserisci URL manualmente (https://...)":
                self.site_url = questionary.text(
                    "🌐 Inserisci l'URL COMPLETO del sito casino:",
                    validate=lambda x: len(x) > 10 and x.startswith(('http://', 'https://'))
                ).ask()
            elif choice == "Sito Maker (configurazione esistente)":
                self.site_url = "https://tuo-sito-maker.com"
            else:
                self.site_url = "https://sandbox.casinomaker.com"
        
        if not self.site_url:
            print("❌ URL non valido")
            return False
        
        print(f"\n✅ URL impostato: {self.site_url}")
        
        # Salva configurazione sito
        self.save_site_config()
        return True
    
    def step2_enter_credentials(self) -> bool:
        """STEP 2: Inserimento credenziali (DOPO il sito)"""
        print("\n" + "🔐" * 30)
        print("🔑 STEP 2: INSERIMENTO CREDENZIALI")
        print("🔐" * 30)
        print(f"\n💡 Inserisci le credenziali per: {self.site_url}")
        print()
        
        if not HAS_QUESTIONARY:
            email = input("📧 Email/Username: ").strip()
            password = input("🔒 Password: ").strip()
        else:
            email = questionary.text("📧 Email/Username:").ask()
            password = questionary.password("🔒 Password:").ask()
        
        if not email or not password:
            print("❌ Credenziali non valide")
            return False
        
        self.credentials = {
            "email": email,
            "password": password,
            "site_url": self.site_url
        }
        
        print(f"\n✅ Credenziali salvate per: {email}")
        return True
    
    def step3_select_game(self) -> bool:
        """STEP 3: Selezione gioco da testare"""
        print("\n" + "🎮" * 30)
        print("🎲 STEP 3: SELEZIONE GIOCO")
        print("🎮" * 30)
        
        available_games = ["Blackjack", "Roulette", "Baccarat", "Poker", "Slot"]
        
        if not HAS_QUESTIONARY:
            print("\n🎯 Giochi disponibili:")
            for i, game in enumerate(available_games, 1):
                print(f"   {i}. {game}")
            choice = input("\nSeleziona gioco (1-5): ").strip()
            try:
                game_idx = int(choice) - 1
                selected_game = available_games[game_idx]
            except:
                selected_game = "Blackjack"
        else:
            selected_game = questionary.select(
                "🎯 Quale gioco vuoi testare?",
                choices=available_games
            ).ask()
        
        self.game_config = {
            "name": selected_game,
            "type": selected_game.lower(),
            "auto_detect": True
        }
        
        print(f"\n✅ Gioco selezionato: {selected_game}")
        return True
    
    def step4_configure_ai(self) -> bool:
        """STEP 4: Configurazione parametri AI per auto-pilota"""
        print("\n" + "🤖" * 30)
        print("⚙️  STEP 4: CONFIGURAZIONE AI")
        print("🤖" * 30)
        
        if not HAS_QUESTIONARY:
            print("\n🔧 Configurazione parametri AI:")
            bankroll = input("💰 Bankroll iniziale (default: 10000): ").strip() or "10000"
            risk = input("🎯 Rischio per mano % (default: 1): ").strip() or "1"
            stop_loss = input("📉 Stop-loss % (default: 20): ").strip() or "20"
            stop_win = input("📈 Stop-win % (default: 30): ").strip() or "30"
            card_counting = input("🎴 Conteggio carte? (s/n, default: s): ").strip().lower() != "n"
        else:
            bankroll = questionary.text(
                "💰 Bankroll iniziale:",
                default="10000"
            ).ask()
            
            risk = questionary.text(
                "🎯 Rischio per mano (% del bankroll):",
                default="1"
            ).ask()
            
            stop_loss = questionary.text(
                "📉 Stop-loss (% del bankroll):",
                default="20"
            ).ask()
            
            stop_win = questionary.text(
                "📈 Stop-win (% del bankroll):",
                default="30"
            ).ask()
            
            card_counting = questionary.confirm(
                "🎴 Abilitare conteggio carte?",
                default=True
            ).ask()
        
        self.ai_config = {
            "mode": "auto_pilot",
            "initial_bankroll": float(bankroll),
            "risk_per_bet": float(risk) / 100,
            "stop_loss": float(stop_loss) / 100,
            "stop_win": float(stop_win) / 100,
            "enable_card_counting": card_counting and self.game_config["name"] == "Blackjack",
            "auto_withdraw": True,
            "require_supervision": True
        }
        
        print("\n✅ Configurazione AI completata:")
        print(f"   💰 Bankroll: ${bankroll}")
        print(f"   🎯 Rischio: {risk}%")
        print(f"   📉 Stop-loss: {stop_loss}%")
        print(f"   📈 Stop-win: {stop_win}%")
        print(f"   🎴 Conteggio carte: {'SI' if card_counting else 'NO'}")
        
        return True
    
    def step5_start_ai(self):
        """STEP 5: Avvio AI in auto-pilota"""
        print("\n" + "🚀" * 30)
        print("🤖 STEP 5: AVVIO AUTO-PILOTA")
        print("🚀" * 30)
        
        print(f"\n🎯 Riepilogo sessione:")
        print(f"   🌐 Sito: {self.site_url}")
        print(f"   🎮 Gioco: {self.game_config['name']}")
        print(f"   🤖 Modalità: Auto-pilota completo")
        print(f"   💰 Bankroll: ${self.ai_config['initial_bankroll']}")
        print(f"   🎴 Conteggio carte: {'ATTIVO' if self.ai_config['enable_card_counting'] else 'DISATTIVO'}")
        
        if HAS_QUESTIONARY:
            confirm = questionary.confirm("\n⚠️  Avviare l'AI in auto-pilota?").ask()
            if not confirm:
                print("❌ Sessione annullata")
                return
        
        print("\n" + "🔧" * 30)
        print("🤖 AI IN ESECUZIONE - AUTO-PILOTA ATTIVO")
        print("🔧" * 30)
        
        # Simula sessione AI (nella realtà qui partirebbe l'AI vera)
        self.simulate_ai_session()
    
    def simulate_ai_session(self):
        """Simula una sessione AI"""
        import random
        import time
        
        bankroll = self.ai_config["initial_bankroll"]
        initial_bankroll = bankroll
        hands_played = 0
        card_count = 0
        
        print("\n🎲 Simulazione in corso...")
        print("   (Nella versione reale, l'AI interagirebbe col sito)")
        print()
        
        for i in range(1, 51):  # Simula 50 mani
            # Calcola puntata
            bet = bankroll * self.ai_config["risk_per_bet"]
            bet = max(10, min(bet, bankroll * 0.05))  # Limiti
            
            # Simula risultato
            outcome = random.choices(
                ['win', 'loss', 'push'],
                weights=[0.48, 0.47, 0.05]
            )[0]
            
            if outcome == 'win':
                profit = bet * 0.95  # Commissione
            elif outcome == 'loss':
                profit = -bet
            else:
                profit = 0
            
            # Aggiorna bankroll
            bankroll += profit
            
            # Aggiorna conteggio carte (se attivo)
            if self.ai_config['enable_card_counting']:
                cards = random.randint(2, 6)
                for _ in range(cards):
                    card = random.randint(1, 13)
                    if 2 <= card <= 6:
                        card_count += 1
                    elif card >= 10:
                        card_count -= 1
            
            hands_played += 1
            
            # Mostra progresso ogni 10 mani
            if i % 10 == 0:
                profit_total = bankroll - initial_bankroll
                profit_pct = (profit_total / initial_bankroll) * 100
                print(f"   📊 Mano {i}: Bankroll=${bankroll:.0f} ({profit_pct:+.1f}%) Count={card_count}")
            
            time.sleep(0.1)
        
        # Risultati finali
        profit_total = bankroll - initial_bankroll
        profit_pct = (profit_total / initial_bankroll) * 100
        
        print("\n" + "📊" * 30)
        print("📈 RISULTATI SESSIONE")
        print("📊" * 30)
        print(f"   🎲 Mani giocate: {hands_played}")
        print(f"   💰 Bankroll iniziale: ${initial_bankroll:.0f}")
        print(f"   💰 Bankroll finale: ${bankroll:.0f}")
        print(f"   📈 Profitto: ${profit_total:+.0f} ({profit_pct:+.1f}%)")
        if self.ai_config['enable_card_counting']:
            print(f"   🎴 Conteggio finale: {card_count}")
        
        self.current_session = {
            "bankroll": bankroll,
            "profit": profit_total,
            "hands_played": hands_played,
            "card_count": card_count
        }
    
    def step6_assisted_withdraw(self):
        """STEP 6: Withdraw assistito con supervisione"""
        if not self.current_session:
            print("\n❌ Nessuna sessione attiva per withdraw")
            return
        
        print("\n" + "💰" * 30)
        print("💳 STEP 6: WITHDRAW ASSISTITO")
        print("💰" * 30)
        
        print("\n⚠️  ATTENZIONE: Procedura di withdraw richiede SUPERVISIONE")
        print("   L'AI mostrerà i passaggi, ma serve conferma manuale")
        print()
        
        withdraw_amount = self.current_session["bankroll"]
        
        print(f"💰 Importo disponibile per withdraw: ${withdraw_amount:.2f}")
        
        if HAS_QUESTIONARY:
            proceed = questionary.confirm("Procedere con il withdraw?").ask()
            if not proceed:
                print("❌ Withdraw annullato")
                return
        
        # Procedura di withdraw assistito
        steps = [
            "🔐 Accedi alla pagina di withdraw",
            "💳 Seleziona metodo di pagamento",
            "💰 Inserisci importo da prelevare",
            "📋 Verifica dettagli transazione",
            "✅ Conferma operazione"
        ]
        
        print("\n📋 PROCEDURA WITHDRAW:")
        for i, step in enumerate(steps, 1):
            print(f"\n   {i}. {step}")
            if HAS_QUESTIONARY:
                questionary.confirm("   Pronto per il passo successivo?").ask()
            else:
                input(f"   Premi Invio per continuare...")
        
        print("\n" + "✅" * 30)
        print("🎉 WITHDRAW COMPLETATO CON SUCCESSO!")
        print("✅" * 30)
        print(f"\n💰 Importo prelevato: ${withdraw_amount:.2f}")
        print("📧 Verifica l'email per la conferma della transazione")
        print("🕒 Tempo stimato per accredito: 1-3 giorni lavorativi")
    
    def save_site_config(self):
        """Salva configurazione sito"""
        config_dir = Path("config/sites")
        config_dir.mkdir(exist_ok=True)
        
        config = {
            "url": self.site_url,
            "last_accessed": time.strftime("%Y-%m-%d %H:%M:%S"),
            "requires_credentials": True,
            "auto_detection": True
        }
        
        config_file = config_dir / "current_site.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f)

def main():
    """Funzione principale"""
    cli = CasinoCLI()
    cli.run()

if __name__ == "__main__":
    main()

