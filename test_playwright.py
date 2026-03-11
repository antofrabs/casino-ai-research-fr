#!/usr/bin/env python3
"""
Test script per verificare l'installazione di Playwright
"""
import sys

print("=" * 60)
print("🧪 TEST INSTALLAZIONE PLAYWRIGHT")
print("=" * 60)
print()

# Test 1: Import Playwright
print("1️⃣ Test import Playwright...")
try:
    from playwright.sync_api import sync_playwright
    print("   ✅ Import OK")
except ImportError as e:
    print(f"   ❌ Import FALLITO: {e}")
    print()
    print("   💡 Installa con:")
    print("      pip install playwright")
    sys.exit(1)

# Test 2: Avvio Playwright
print("2️⃣ Test avvio Playwright...")
try:
    playwright = sync_playwright().start()
    print("   ✅ Playwright avviato")
    playwright.stop()
except Exception as e:
    print(f"   ❌ Avvio FALLITO: {e}")
    sys.exit(1)

# Test 3: Browser disponibile
print("3️⃣ Test browser Chromium...")
try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    print("   ✅ Chromium disponibile")
    browser.close()
    playwright.stop()
except Exception as e:
    print(f"   ❌ Browser FALLITO: {e}")
    print()
    print("   💡 Installa browser con:")
    print("      python3 -m playwright install chromium")
    sys.exit(1)

print()
print("=" * 60)
print("✅ TUTTI I TEST SUPERATI!")
print("=" * 60)
print()
print("🎉 Playwright è installato correttamente!")
print("   Ora puoi usare l'interfaccia web senza problemi.")


















