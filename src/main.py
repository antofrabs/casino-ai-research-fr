#!/usr/bin/env python3
"""
🎰 CASINO AI RESEARCH PLATFORM - Main Entry Point
===============================================================

Flusso CORRETTO per valutazione:
1. PRIMA: Inserimento sito (URL https://...)
2. POI: Credenziali (email, password)
3. POI: Selezione gioco
4. POI: Configurazione parametri AI
5. POI: Auto-pilota completo con conteggio carte
6. SUPERVISIONE: Withdraw assistito
"""
import sys
import os
import subprocess
from pathlib import Path

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    print("=" * 70)
    print("🎰 CASINO AI RESEARCH PLATFORM - VERSIONE VALUTAZIONE")
    print("=" * 70)
    print()
    print("⚠️  IMPORTANTE: Questo software è solo per scopi di ricerca.")
    print("   Usare solo su siti di proprietà o con permesso esplicito.")
    print()
    
    # Mostra opzioni
    print("📋 MODALITÀ DISPONIBILI:")
    print("   1. 🌐 Interfaccia Web (consigliato)")
    print("   2. 💻 Interfaccia CLI (terminale)")
    print()
    
    # Verifica se streamlit è disponibile
    try:
        import streamlit
        has_streamlit = True
    except ImportError:
        has_streamlit = False
        print("⚠️  Streamlit non installato. Installa con: pip install streamlit")
        print()
    
    if has_streamlit:
        # Verifica Playwright prima
        try:
            from playwright.sync_api import sync_playwright
            playwright_ok = True
        except ImportError:
            playwright_ok = False
            print()
            print("⚠️  ATTENZIONE: Playwright non installato!")
            print("   L'interfaccia web richiede Playwright per funzionare.")
            print()
            print("💡 Installa con:")
            print("   pip install playwright")
            print("   python3 -m playwright install chromium")
            print()
            choice = input("Vuoi continuare comunque? (s/n, default=n): ").strip().lower() or "n"
            if choice != "s":
                return 1
        
        choice = input("Scegli modalità (1=Web, 2=CLI, default=Web): ").strip() or "1"
        
        if choice == "1":
            # Avvia interfaccia web
            web_file = Path(__file__).parent.parent / "src" / "dashboard" / "web_interface.py"
            
            if web_file.exists():
                print()
                print("🌐 Avvio interfaccia web...")
                print("📱 Il browser si aprirà automaticamente")
                print("🔗 URL: http://localhost:8501")
                print("⚠️  Per fermare il server, premi Ctrl+C")
                print()
                
                # Verifica Playwright una volta ancora
                if not playwright_ok:
                    print("❌ Playwright non disponibile. Avvio comunque ma il browser non funzionerà.")
                    print()
                
                import webbrowser
                import threading
                import time
                
                def open_browser():
                    time.sleep(3)
                    webbrowser.open("http://localhost:8501")
                
                browser_thread = threading.Thread(target=open_browser, daemon=True)
                browser_thread.start()
                
                subprocess.run([
                    sys.executable, "-m", "streamlit", "run",
                    str(web_file),
                    "--server.port", "8501",
                    "--server.headless", "false",
                    "--browser.gatherUsageStats", "false"
                ])
                return 0
            else:
                print(f"❌ File interfaccia web non trovato: {web_file}")
                print("   Passo alla modalità CLI...")
                print()
    
    # Modalità CLI
    print("📋 FLUSSO OPERATIVO:")
    print("   1. 📍 Selezione sito casino (URL https://...)")
    print("   2. 🔐 Inserimento credenziali")
    print("   3. 🎮 Selezione gioco (Blackjack, Roulette, ecc.)")
    print("   4. 🤖 Configurazione parametri AI")
    print("   5. 🚀 Avvio auto-pilota con conteggio carte")
    print("   6. 💰 Withdraw assistito con supervisione")
    print()
    
    try:
        from src.ui.cli_interface import CasinoCLI
        cli = CasinoCLI()
        cli.run()
    except ImportError as e:
        print(f"❌ Errore: {e}")
        print("Installa le dipendenze con: pip install -r requirements.txt")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

