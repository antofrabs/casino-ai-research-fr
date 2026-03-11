#!/usr/bin/env python3
"""
Demo del Casino AI Research Platform
Mostra il funzionamento completo senza input interattivo
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.cli_interface import CasinoCLI

class DemoCLI(CasinoCLI):
    """Versione demo che usa valori predefiniti"""
    
    def step1_select_site(self) -> bool:
        """Demo: usa sito di test"""
        print("\n" + "🔗" * 30)
        print("🎯 STEP 1: SELEZIONE SITO CASINO")
        print("🔗" * 30)
        self.site_url = "https://demo-casino.com"
        print(f"\n✅ URL impostato: {self.site_url}")
        self.save_site_config()
        return True
    
    def step2_enter_credentials(self) -> bool:
        """Demo: usa credenziali di test"""
        print("\n" + "🔐" * 30)
        print("🔑 STEP 2: INSERIMENTO CREDENZIALI")
        print("🔐" * 30)
        self.credentials = {
            "email": "demo@example.com",
            "password": "demo123",
            "site_url": self.site_url
        }
        print(f"\n✅ Credenziali salvate per: {self.credentials['email']}")
        return True
    
    def step3_select_game(self) -> bool:
        """Demo: seleziona Blackjack"""
        print("\n" + "🎮" * 30)
        print("🎲 STEP 3: SELEZIONE GIOCO")
        print("🎮" * 30)
        self.game_config = {
            "name": "Blackjack",
            "type": "blackjack",
            "auto_detect": True
        }
        print(f"\n✅ Gioco selezionato: {self.game_config['name']}")
        return True
    
    def step4_configure_ai(self) -> bool:
        """Demo: configurazione AI predefinita"""
        print("\n" + "🤖" * 30)
        print("⚙️  STEP 4: CONFIGURAZIONE AI")
        print("🤖" * 30)
        self.ai_config = {
            "mode": "auto_pilot",
            "initial_bankroll": 10000.0,
            "risk_per_bet": 0.01,
            "stop_loss": 0.2,
            "stop_win": 0.3,
            "enable_card_counting": True,
            "auto_withdraw": True,
            "require_supervision": True
        }
        print("\n✅ Configurazione AI completata:")
        print(f"   💰 Bankroll: $10000")
        print(f"   🎯 Rischio: 1%")
        print(f"   📉 Stop-loss: 20%")
        print(f"   📈 Stop-win: 30%")
        print(f"   🎴 Conteggio carte: SI")
        return True
    
    def step6_assisted_withdraw(self):
        """Demo: mostra procedura withdraw senza input"""
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
            import time
            time.sleep(0.5)  # Simula attesa
        
        print("\n" + "✅" * 30)
        print("🎉 WITHDRAW COMPLETATO CON SUCCESSO!")
        print("✅" * 30)
        print(f"\n💰 Importo prelevato: ${withdraw_amount:.2f}")
        print("📧 Verifica l'email per la conferma della transazione")
        print("🕒 Tempo stimato per accredito: 1-3 giorni lavorativi")

if __name__ == "__main__":
    print("=" * 70)
    print("🎰 CASINO AI RESEARCH PLATFORM - DEMO MODE")
    print("=" * 70)
    print()
    print("⚠️  MODALITÀ DEMO: Usa valori predefiniti per dimostrazione")
    print()
    
    cli = DemoCLI()
    cli.run()

