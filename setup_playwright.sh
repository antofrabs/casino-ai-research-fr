#!/bin/bash
# Script per installare Playwright in ambienti cloud

echo "🎭 Installazione Playwright per ambiente cloud..."

# Installa Playwright
pip install playwright

# Installa browser Chromium
playwright install chromium

# Installa dipendenze di sistema (se necessario)
playwright install-deps chromium

echo "✅ Playwright installato correttamente!"

