# 🚀 Guida al Deploy Online - Casino AI Research Platform

Questa guida ti aiuta a pubblicare l'applicazione online su vari servizi cloud.

## 📋 Indice

1. [Streamlit Cloud](#streamlit-cloud) ⭐ **Consigliato - Gratuito e Facile**
2. [Heroku](#heroku)
3. [Docker (AWS/Google Cloud/Azure)](#docker)
4. [Railway](#railway)
5. [Render](#render)

---

## 🌐 Streamlit Cloud (Consigliato)

**Vantaggi**: Gratuito, facile, ottimizzato per Streamlit

### Prerequisiti
- Account GitHub
- Repository GitHub con il codice

### Passi

1. **Prepara il repository GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/tuonome/casino-ai-research.git
   git push -u origin main
   ```

2. **Vai su [Streamlit Cloud](https://streamlit.io/cloud)**
   - Accedi con GitHub
   - Clicca "New app"

3. **Configura l'app**
   - **Repository**: Seleziona il tuo repo
   - **Branch**: `main` (o `master`)
   - **Main file path**: `src/dashboard/web_interface.py`
   - **Python version**: 3.11

4. **Deploy!**
   - Clicca "Deploy"
   - Attendi il build (2-5 minuti)
   - L'app sarà disponibile su `https://tuonome-casino-ai-research.streamlit.app`

### ⚠️ Note Importanti per Streamlit Cloud

- **Playwright**: Potrebbe richiedere configurazione speciale
- **Browser**: In modalità headless automatica
- **Limiti**: Gratuito ha limiti di CPU/RAM

### File Necessari
- ✅ `requirements.txt` (o `requirements-cloud.txt`)
- ✅ `.streamlit/config.toml`
- ✅ `src/dashboard/web_interface.py`

---

## 🟣 Heroku

**Vantaggi**: Popolare, flessibile, buona documentazione

### Prerequisiti
- Account Heroku
- Heroku CLI installato
- Git

### Passi

1. **Installa Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Crea app Heroku**
   ```bash
   cd casino-ai-research
   heroku create casino-ai-research
   ```

4. **Configura buildpack**
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add heroku-community/apt
   ```

5. **Crea file `Aptfile`** (per dipendenze sistema Playwright)
   ```
   libnss3
   libatk1.0-0
   libatk-bridge2.0-0
   libcups2
   libdrm2
   libxkbcommon0
   libxcomposite1
   libxdamage1
   libxfixes3
   libxrandr2
   libgbm1
   libasound2
   libpango-1.0-0
   libcairo2
   ```

6. **Aggiungi script di build** (`bin/post_compile`)
   ```bash
   #!/bin/bash
   playwright install chromium
   playwright install-deps chromium
   ```

7. **Deploy**
   ```bash
   git add .
   git commit -m "Prepare for Heroku"
   git push heroku main
   ```

8. **Apri l'app**
   ```bash
   heroku open
   ```

### Variabili d'Ambiente (se necessario)
```bash
heroku config:set PYTHONUNBUFFERED=1
heroku config:set STREAMLIT_SERVER_HEADLESS=true
```

---

## 🐳 Docker (AWS/Google Cloud/Azure)

**Vantaggi**: Massima flessibilità, controllo totale

### Prerequisiti
- Docker installato
- Account su AWS/GCP/Azure

### Build Locale

1. **Build immagine**
   ```bash
   docker build -t casino-ai-research .
   ```

2. **Test locale**
   ```bash
   docker run -p 8501:8501 casino-ai-research
   ```

3. **Push su registry**
   ```bash
   # Esempio per AWS ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
   docker tag casino-ai-research:latest <account>.dkr.ecr.us-east-1.amazonaws.com/casino-ai-research:latest
   docker push <account>.dkr.ecr.us-east-1.amazonaws.com/casino-ai-research:latest
   ```

### Deploy su AWS (ECS/Fargate)

1. **Crea cluster ECS**
2. **Crea task definition** usando l'immagine Docker
3. **Crea servizio** e avvia

### Deploy su Google Cloud Run

```bash
# Build e push
gcloud builds submit --tag gcr.io/PROJECT-ID/casino-ai-research

# Deploy
gcloud run deploy casino-ai-research \
  --image gcr.io/PROJECT-ID/casino-ai-research \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Deploy su Azure Container Instances

```bash
# Login
az login

# Crea resource group
az group create --name casino-ai-rg --location eastus

# Deploy container
az container create \
  --resource-group casino-ai-rg \
  --name casino-ai-research \
  --image casino-ai-research:latest \
  --dns-name-label casino-ai-research \
  --ports 8501
```

---

## 🚂 Railway

**Vantaggi**: Moderno, facile, buon free tier

### Passi

1. **Vai su [Railway](https://railway.app)**
2. **Connetti GitHub**
3. **Crea nuovo progetto** dal repository
4. **Railway rileva automaticamente**:
   - Dockerfile (se presente)
   - requirements.txt
   - Procfile

5. **Configura variabili** (se necessario)
6. **Deploy automatico!**

### File Necessari
- ✅ `Dockerfile` (consigliato)
- ✅ `requirements.txt`
- ✅ `Procfile` (alternativa)

---

## 🎨 Render

**Vantaggi**: Facile, buon free tier, buona UX

### Passi

1. **Vai su [Render](https://render.com)**
2. **Connetti GitHub**
3. **Crea nuovo Web Service**
4. **Configura**:
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `streamlit run src/dashboard/web_interface.py --server.port=$PORT --server.address=0.0.0.0`
   - **Environment**: Python 3

5. **Deploy!**

---

## ⚙️ Configurazioni Comuni

### Variabili d'Ambiente

Crea file `.env` o configura nel servizio:

```env
PYTHONUNBUFFERED=1
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Ottimizzazioni

1. **Usa `requirements-cloud.txt`** invece di `requirements.txt` per deploy più veloci
2. **Rimuovi dipendenze non necessarie** (tensorflow, torch se non usati)
3. **Usa build cache** quando possibile

---

## 🔧 Troubleshooting

### Playwright non funziona in cloud

**Problema**: Playwright richiede browser installati

**Soluzione**:
```bash
# Aggiungi al Dockerfile o script di build
playwright install chromium
playwright install-deps chromium
```

### Porta non disponibile

**Problema**: Errore "Port already in use"

**Soluzione**: Usa variabile `$PORT` (Heroku/Railway) o porta dinamica

### Memoria insufficiente

**Problema**: App si blocca o crasha

**Soluzione**:
- Usa `requirements-cloud.txt` (più leggero)
- Aumenta risorse nel piano cloud
- Ottimizza codice (rimuovi import non usati)

### Build lento

**Problema**: Build richiede troppo tempo

**Soluzione**:
- Usa build cache
- Riduci dipendenze
- Usa multi-stage Docker build

---

## 📊 Confronto Servizi

| Servizio | Free Tier | Facilità | Playwright | Consigliato |
|----------|-----------|----------|------------|-------------|
| **Streamlit Cloud** | ✅ Sì | ⭐⭐⭐⭐⭐ | ⚠️ Limitato | ⭐⭐⭐⭐⭐ |
| **Heroku** | ⚠️ Limitato | ⭐⭐⭐⭐ | ✅ Sì | ⭐⭐⭐⭐ |
| **Railway** | ✅ Sì | ⭐⭐⭐⭐⭐ | ✅ Sì | ⭐⭐⭐⭐⭐ |
| **Render** | ✅ Sì | ⭐⭐⭐⭐ | ✅ Sì | ⭐⭐⭐⭐ |
| **AWS/GCP/Azure** | ⚠️ No | ⭐⭐ | ✅ Sì | ⭐⭐⭐ |

---

## 🎯 Raccomandazione

**Per iniziare**: **Streamlit Cloud** (gratuito, facile, ottimizzato)

**Per produzione**: **Railway** o **Render** (più flessibili, buon supporto Playwright)

**Per enterprise**: **AWS/GCP/Azure** con Docker (massimo controllo)

---

## 📝 Checklist Pre-Deploy

- [ ] Codice su GitHub
- [ ] `requirements.txt` aggiornato
- [ ] `.streamlit/config.toml` configurato
- [ ] Testato localmente
- [ ] Playwright installato correttamente
- [ ] Variabili d'ambiente configurate
- [ ] Documentazione aggiornata

---

**Buon deploy! 🚀**

