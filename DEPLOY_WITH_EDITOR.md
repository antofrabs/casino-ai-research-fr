# 🌐 Deploy Online con Editor di Codice Integrato

## ✅ Funzionalità Implementata

L'applicazione ora include un **editor di codice integrato** che permette di modificare il codice direttamente dall'interfaccia web, anche quando è deployata online.

## 🎯 Come Funziona

### 1. **Accesso Editor**
- Clicca su **"📝 Apri Editor"** nella sidebar
- Seleziona il file Python da modificare
- Modifica il codice direttamente nell'interfaccia

### 2. **Funzionalità Editor**
- ✅ **Syntax highlighting** (se `streamlit-ace` installato)
- ✅ **Salvataggio file** con backup automatico
- ✅ **Ripristino** del contenuto originale
- ✅ **Visualizzazione backup** disponibili
- ✅ **Ricarica moduli** Python dopo modifica
- ✅ **Anteprima modifiche** prima di salvare

### 3. **Sicurezza**
- ⚠️ **Backup automatico** prima di ogni salvataggio
- ⚠️ **Conferma visiva** delle modifiche
- ⚠️ **Ripristino** sempre disponibile

## 🚀 Deploy Online

### Opzione 1: Streamlit Cloud (Consigliato)

1. **Prepara repository GitHub**
   ```bash
   git init
   git add .
   git commit -m "Casino AI Platform with Code Editor"
   git remote add origin https://github.com/tuonome/casino-ai-research.git
   git push -u origin main
   ```

2. **Deploy su Streamlit Cloud**
   - Vai su [streamlit.io/cloud](https://streamlit.io/cloud)
   - Connetti GitHub
   - Seleziona repository
   - Main file: `src/dashboard/web_interface.py`
   - Deploy!

3. **Accesso Editor**
   - Una volta deployato, accedi all'app
   - Clicca "📝 Apri Editor" nella sidebar
   - Modifica i file direttamente online!

### Opzione 2: Heroku

1. **Aggiungi Procfile** (già presente)
   ```
   web: streamlit run src/dashboard/web_interface.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy**
   ```bash
   heroku create casino-ai-research
   git push heroku main
   heroku open
   ```

### Opzione 3: Railway

1. **Connetti GitHub** su [railway.app](https://railway.app)
2. **Deploy automatico** - Railway rileva Streamlit
3. **Accesso editor** - Funziona automaticamente!

### Opzione 4: Docker (AWS/GCP/Azure)

1. **Build immagine**
   ```bash
   docker build -t casino-ai-research .
   ```

2. **Deploy** su servizio cloud preferito
3. **Editor funziona** - Modifiche salvate nel container

## ⚙️ Configurazione

### Variabili d'Ambiente

```env
# Permessi scrittura file (necessario per editor)
ALLOW_FILE_WRITES=true

# Directory modificabile
EDITABLE_DIR=./src
```

### Permessi File System

L'editor richiede **permessi di scrittura** sui file. Assicurati che:
- I file siano scrivibili dal processo Streamlit
- La directory non sia read-only
- Ci sia spazio su disco per i backup

## 🔒 Sicurezza

### ⚠️ IMPORTANTE

L'editor di codice permette di **modificare il codice in produzione**. Considera:

1. **Autenticazione**: Aggiungi login se necessario
2. **Autorizzazione**: Limita accesso all'editor
3. **Backup**: I backup vengono salvati localmente
4. **Versioning**: Considera Git per tracciare modifiche

### Raccomandazioni

- ✅ Usa solo su server privati o con autenticazione
- ✅ Limita accesso all'editor a utenti autorizzati
- ✅ Fai backup regolari del codice
- ✅ Usa Git per versioning
- ⚠️ Non usare in produzione pubblica senza sicurezza

## 📝 Esempio Uso

1. **Accedi all'app** deployata online
2. **Clicca "📝 Apri Editor"** nella sidebar
3. **Seleziona file** da modificare (es. `src/automation/browser_controller.py`)
4. **Modifica codice** nell'editor
5. **Clicca "💾 Salva File"**
6. **Backup creato** automaticamente
7. **Modulo ricaricato** se applicabile
8. **Modifiche attive** immediatamente!

## 🛠️ Troubleshooting

### Editor non si apre
- Verifica che `streamlit-ace` sia installato: `pip install streamlit-ace`
- Controlla console browser per errori

### File non salvabile
- Verifica permessi di scrittura
- Controlla che il percorso file sia corretto
- Verifica spazio su disco

### Modifiche non applicate
- Ricarica la pagina dopo salvataggio
- Verifica che il modulo sia stato ricaricato
- Controlla log per errori

## 🎯 Vantaggi

- ✅ **Modifica online**: Cambia codice senza SSH/FTP
- ✅ **Backup automatico**: Sicurezza integrata
- ✅ **Ricarica moduli**: Modifiche attive subito
- ✅ **Interface intuitiva**: Editor con syntax highlighting
- ✅ **Multi-file**: Modifica qualsiasi file Python

---

**Ora puoi modificare il codice direttamente dall'applicazione online! 💻**
