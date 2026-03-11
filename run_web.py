#!/usr/bin/env python3
"""
🚀 Avvia l'interfaccia web del Casino AI Research Platform
===============================================================

Questo script avvia automaticamente il browser con l'interfaccia web
"""
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    """Avvia l'interfaccia web Streamlit"""
    print("=" * 70)
    print("🎰 CASINO AI RESEARCH PLATFORM - WEB INTERFACE")
    print("=" * 70)
    print()
    print("🌐 Avvio interfaccia web...")
    print("📱 Il browser si aprirà automaticamente")
    print("🔗 URL: http://localhost:8501")
    print()
    print("⚠️  Per fermare il server, premi Ctrl+C")
    print()
    
    # Path al file dell'interfaccia web
    web_file = Path(__file__).parent / "src" / "dashboard" / "web_interface.py"
    
    if not web_file.exists():
        print(f"❌ File non trovato: {web_file}")
        return 1
    
    # Apri browser dopo un breve delay
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:8501")
    
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Avvia Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(web_file),
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server fermato")
        return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(main())




















