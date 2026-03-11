# 🔧 Risoluzione Problemi

## ❌ Errore: "Impossibile avviare il browser. Installa Playwright"

### Problema 1: Playwright non installato

**Sintomi:**
- Errore quando provi ad avviare il browser
- Messaggio: "Playwright not installed"

**Soluzione:**
```bash
cd casino-ai-research
pip install playwright
python3 -m playwright install chromium
```

### Problema 2: Streamlit usa Python diverso

**Sintomi:**
- Playwright funziona quando lo testi direttamente
- Ma non funziona nell'interfaccia web Streamlit

**Soluzione:**

1. **Verifica quale Python usa Streamlit:**
```bash
# In un terminale, avvia Streamlit e guarda l'output
streamlit run src/dashboard/web_interface.py
# Cerca la riga che mostra il path di Python
```

2. **Installa Playwright nello stesso ambiente:**
```bash
# Usa lo stesso Python che usa Streamlit
/path/to/python3 -m pip install playwright
/path/to/python3 -m playwright install chromium
```

3. **Oppure usa un ambiente virtuale:**
```bash
# Crea ambiente virtuale
python3 -m venv venv

# Attiva ambiente
source venv/bin/activate  # macOS/Linux
# oppure
venv\Scripts\activate  # Windows

# Installa tutto
pip install -r requirements.txt
pip install playwright
playwright install chromium

# Avvia Streamlit dall'ambiente virtuale
streamlit run src/dashboard/web_interface.py
```

### Problema 3: Browser non si apre

**Sintomi:**
- Nessun errore ma il browser non si apre
- Il processo si blocca

**Soluzione:**

1. **Verifica che Chromium sia installato:**
```bash
python3 -m playwright install chromium
```

2. **Testa manualmente:**
```bash
python3 test_playwright.py
```

3. **Verifica permessi (macOS):**
- Vai su: Preferenze di Sistema > Sicurezza e Privacy
- Assicurati che Terminal/Python abbia i permessi necessari

### Problema 4: Interfaccia web non si apre

**Sintomi:**
- Il comando `python3 src/main.py` non apre il browser

**Soluzione:**

1. **Apri manualmente:**
```bash
# Avvia Streamlit direttamente
streamlit run src/dashboard/web_interface.py

# Poi apri manualmente nel browser:
# http://localhost:8501
```

2. **Verifica che la porta sia libera:**
```bash
# Se la porta 8501 è occupata, usa un'altra porta
streamlit run src/dashboard/web_interface.py --server.port 8502
```

## 🧪 Test Diagnostici

### Test Completo
```bash
python3 diagnostica.py
```

Questo script verifica:
- ✅ Installazione Python
- ✅ Playwright installato e funzionante
- ✅ Moduli del progetto
- ✅ Streamlit
- ✅ File necessari

### Test Playwright
```bash
python3 test_playwright.py
```

Questo test verifica solo Playwright.

## 🔍 Debug Avanzato

### Verifica ambiente Python
```bash
# Quale Python stai usando?
which python3
python3 --version

# Quale pip?
which pip3
pip3 --version

# Lista pacchetti installati
pip3 list | grep playwright
```

### Reinstallazione completa
```bash
# Disinstalla
pip3 uninstall playwright

# Reinstalla
pip3 install playwright
python3 -m playwright install chromium

# Verifica
python3 test_playwright.py
```

## 💡 Suggerimenti

1. **Usa sempre lo stesso Python:**
   - Se usi `python3` per installare, usa `python3` per eseguire
   - Se usi un venv, attivalo sempre prima

2. **Riavvia dopo installazioni:**
   - Dopo aver installato Playwright, riavvia Streamlit
   - Chiudi e riapri il terminale se necessario

3. **Controlla i log:**
   - Streamlit mostra errori nella console
   - Cerca messaggi di errore specifici

4. **Ambiente virtuale consigliato:**
```bash
# Crea venv
python3 -m venv venv
source venv/bin/activate

# Installa tutto
pip install -r requirements.txt
pip install playwright
playwright install chromium

# Avvia
streamlit run src/dashboard/web_interface.py
```

## 🆘 Se Nulla Funziona

1. Esegui la diagnostica completa:
```bash
python3 diagnostica.py
```

2. Controlla i log di errore completi

3. Verifica che tutti i file siano presenti:
```bash
ls -la src/automation/browser_controller.py
ls -la src/dashboard/web_interface.py
```

4. Prova a reinstallare tutto:
```bash
pip3 install --upgrade playwright
python3 -m playwright install --force chromium
```

---

**Se il problema persiste, condividi l'output di `python3 diagnostica.py`**


















