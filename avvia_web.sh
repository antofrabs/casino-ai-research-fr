#!/bin/bash
# Script per avviare l'interfaccia web con verifiche

echo "🎰 Casino AI Research Platform - Avvio Interfaccia Web"
echo "======================================================"
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato!"
    exit 1
fi

echo "✅ Python trovato: $(python3 --version)"
echo ""

# Verifica Playwright
echo "🔍 Verifica Playwright..."
if python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    echo "✅ Playwright installato"
else
    echo "❌ Playwright non installato!"
    echo ""
    echo "💡 Installa con:"
    echo "   pip install playwright"
    echo "   python3 -m playwright install chromium"
    exit 1
fi

# Verifica browser
echo "🔍 Verifica browser Chromium..."
if python3 -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); b = p.chromium.launch(headless=True); b.close(); p.stop()" 2>/dev/null; then
    echo "✅ Browser Chromium disponibile"
else
    echo "❌ Browser Chromium non disponibile!"
    echo ""
    echo "💡 Installa con:"
    echo "   python3 -m playwright install chromium"
    exit 1
fi

echo ""
echo "✅ Tutte le verifiche superate!"
echo ""
echo "🌐 Avvio interfaccia web..."
echo "📱 Il browser si aprirà automaticamente su http://localhost:8501"
echo "⚠️  Per fermare, premi Ctrl+C"
echo ""

# Avvia Streamlit
cd "$(dirname "$0")"
python3 -m streamlit run src/dashboard/web_interface.py \
    --server.port 8501 \
    --server.headless false \
    --browser.gatherUsageStats false


















