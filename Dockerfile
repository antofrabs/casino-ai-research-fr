# 🎰 Casino AI Research Platform - Dockerfile
# Per deploy su servizi cloud (Heroku, AWS, Google Cloud, etc.)

FROM python:3.11-slim

# Imposta variabili d'ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Installa dipendenze di sistema per Playwright e altre librerie
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Crea directory di lavoro
WORKDIR /app

# Copia requirements e installa dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Installa browser Playwright
RUN playwright install chromium && \
    playwright install-deps chromium

# Copia tutto il codice dell'applicazione
COPY . .

# Crea directory necessarie
RUN mkdir -p data/logs data/simulations data/live_sessions data/training_data

# Esponi la porta
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501/_stcore/health')" || exit 1

# Comando per avviare Streamlit
CMD ["streamlit", "run", "src/dashboard/web_interface.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

