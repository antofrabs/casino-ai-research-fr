#!/usr/bin/env python3
"""
Script di diagnostica per problemi con Playwright e Streamlit
"""
import sys
import os
from pathlib import Path

print("=" * 70)
print("🔍 DIAGNOSTICA CASINO AI RESEARCH PLATFORM")
print("=" * 70)
print()

# 1. Info Python
print("1️⃣ INFORMAZIONI PYTHON")
print("-" * 70)
print(f"   Eseguibile: {sys.executable}")
print(f"   Versione: {sys.version}")
print(f"   Path: {sys.path[:3]}...")
print()

# 2. Test Playwright
print("2️⃣ TEST PLAYWRIGHT")
print("-" * 70)
try:
    from playwright.sync_api import sync_playwright
    print("   ✅ Import Playwright: OK")
    
    # Test avvio
    playwright = sync_playwright().start()
    print("   ✅ Avvio Playwright: OK")
    
    # Test browser
    browser = playwright.chromium.launch(headless=True)
    print("   ✅ Browser Chromium: OK")
    browser.close()
    playwright.stop()
    
    print()
    print("   ✅ Playwright funziona correttamente!")
    
except ImportError as e:
    print(f"   ❌ Import FALLITO: {e}")
    print()
    print("   💡 SOLUZIONE:")
    print("      pip install playwright")
    print("      python3 -m playwright install chromium")
    sys.exit(1)
    
except Exception as e:
    print(f"   ❌ Errore: {e}")
    print()
    print("   💡 SOLUZIONE:")
    print("      python3 -m playwright install chromium")
    sys.exit(1)

# 3. Test import moduli progetto
print()
print("3️⃣ TEST MODULI PROGETTO")
print("-" * 70)
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from src.automation.browser_controller import CasinoBrowserController
    print("   ✅ Import CasinoBrowserController: OK")
    
    # Test creazione controller
    controller = CasinoBrowserController(headless=True, slow_mo=50)
    print("   ✅ Creazione Controller: OK")
    
except Exception as e:
    print(f"   ❌ Errore: {e}")
    import traceback
    traceback.print_exc()

# 4. Test Streamlit
print()
print("4️⃣ TEST STREAMLIT")
print("-" * 70)
try:
    import streamlit as st
    print("   ✅ Streamlit installato")
    print(f"   Versione: {st.__version__}")
except ImportError:
    print("   ❌ Streamlit non installato")
    print("   💡 Installa con: pip install streamlit")

# 5. Verifica file
print()
print("5️⃣ VERIFICA FILE")
print("-" * 70)
files_to_check = [
    "src/automation/browser_controller.py",
    "src/dashboard/web_interface.py",
    "config/sites/play_money_sites.yaml"
]

for file_path in files_to_check:
    full_path = Path(__file__).parent / file_path
    if full_path.exists():
        print(f"   ✅ {file_path}")
    else:
        print(f"   ❌ {file_path} (NON TROVATO)")

print()
print("=" * 70)
print("✅ DIAGNOSTICA COMPLETATA")
print("=" * 70)
print()
print("💡 Se Playwright funziona qui ma non in Streamlit:")
print("   1. Verifica che Streamlit usi lo stesso Python")
print("   2. Riavvia Streamlit dopo l'installazione")
print("   3. Controlla che non ci siano ambienti virtuali diversi")
print()


















