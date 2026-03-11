# 🚀 Come Avviare il Sistema

## ⚠️ IMPORTANTE: Entra nella cartella corretta!

Tutti i comandi devono essere eseguiti **dentro la cartella `casino-ai-research`**:

```bash
cd casino-ai-research
```

## 📋 Comandi Disponibili

### 1. Diagnostica Completa
```bash
cd casino-ai-research
python3 diagnostica.py
```

### 2. Test Playwright
```bash
cd casino-ai-research
python3 test_playwright.py
```

### 3. Avvia Interfaccia Web (Metodo 1 - Consigliato)
```bash
cd casino-ai-research
python3 src/main.py
# Scegli opzione 1 quando richiesto
```

### 4. Avvia Interfaccia Web (Metodo 2 - Script)
```bash
cd casino-ai-research
./avvia_web.sh
```

### 5. Avvia Interfaccia Web (Metodo 3 - Diretto)
```bash
cd casino-ai-research
streamlit run src/dashboard/web_interface.py
```

## 🔍 Verifica che sei nella cartella giusta

Prima di eseguire qualsiasi comando, verifica:

```bash
pwd
# Dovresti vedere: .../casino-ai-research

ls diagnostica.py
# Dovresti vedere: diagnostica.py
```

Se non vedi `diagnostica.py`, sei nella cartella sbagliata!

## 📁 Struttura Cartelle

```
untitled folder/
└── casino-ai-research/    ← DEVI ESSERE QUI
    ├── diagnostica.py
    ├── test_playwright.py
    ├── avvia_web.sh
    ├── src/
    └── ...
```

## ✅ Sequenza Corretta

1. **Apri terminale**
2. **Vai nella cartella:**
   ```bash
   cd "/Users/lorenzoantonelli/untitled folder/casino-ai-research"
   ```
3. **Verifica che sei nel posto giusto:**
   ```bash
   ls diagnostica.py
   ```
4. **Esegui diagnostica:**
   ```bash
   python3 diagnostica.py
   ```
5. **Avvia il sistema:**
   ```bash
   python3 src/main.py
   ```

## 🆘 Se Continui ad Avere Problemi

Se il file non viene trovato anche dopo essere entrato in `casino-ai-research`:

```bash
# Verifica che il file esista
ls -la diagnostica.py

# Se non esiste, elenca tutti i file
ls -la

# Verifica la struttura
find . -name "diagnostica.py"
```

---

**Ricorda: sempre `cd casino-ai-research` prima di eseguire i comandi!**
