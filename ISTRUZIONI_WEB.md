# 🌐 Interfaccia Web - Istruzioni

## 🚀 Come Avviare

### Metodo 1: Tramite main.py (Consigliato)
```bash
cd casino-ai-research
python3 src/main.py
```
Quando richiesto, scegli **opzione 1** (Interfaccia Web)

### Metodo 2: Direttamente
```bash
python3 run_web.py
```

### Metodo 3: Con Streamlit
```bash
streamlit run src/dashboard/web_interface.py
```

## 📱 Cosa Succede

1. **Il browser si apre automaticamente** su `http://localhost:8501`
2. Vedi l'interfaccia web completa con tutti i passaggi
3. Compili i form per ogni step
4. Vedi i risultati in tempo reale

## 🎯 Flusso nell'Interfaccia Web

### STEP 1: Selezione Sito Casino
- Inserisci l'URL del sito casino
- Oppure usa le opzioni rapide (Sito Maker, Sito Test)

### STEP 2: Credenziali
- Inserisci email/username e password
- Oppure usa "Salva Demo" per valori di test

### STEP 3: Selezione Gioco
- Scegli tra Blackjack, Roulette, Baccarat, Poker, Slot
- Usa i pulsanti radio per selezionare

### STEP 4: Configurazione AI
- **Bankroll iniziale**: Quanto vuoi investire
- **Rischio per mano**: Percentuale del bankroll per ogni mano
- **Stop-loss**: Percentuale di perdita massima
- **Stop-win**: Percentuale di vincita target
- **Conteggio carte**: Disponibile solo per Blackjack

### STEP 5: Auto-Pilota
- Clicca "Avvia Simulazione"
- Vedi il progresso in tempo reale
- Grafico del bankroll e profitto
- Risultati finali della sessione

### STEP 6: Withdraw Assistito
- Procedura guidata per il prelievo
- Conferma manuale richiesta
- Dettagli della transazione

## 🎨 Caratteristiche Interfaccia

- ✅ **Design moderno** con colori casino
- ✅ **Progresso visivo** nella sidebar
- ✅ **Grafici in tempo reale** del bankroll
- ✅ **Metriche dettagliate** per ogni step
- ✅ **Responsive** - funziona su desktop e mobile
- ✅ **Auto-save** - i dati vengono salvati durante la sessione

## 🔧 Risoluzione Problemi

### Il browser non si apre
Apri manualmente: `http://localhost:8501`

### Porta già in uso
```bash
streamlit run src/dashboard/web_interface.py --server.port 8502
```

### Errore "Module not found"
```bash
pip install streamlit pandas pyyaml
```

## 💡 Suggerimenti

- Usa "Salva Demo" per testare rapidamente
- Il conteggio carte è disponibile solo per Blackjack
- I dati vengono salvati solo durante la sessione corrente
- Puoi tornare indietro in qualsiasi momento
- Usa "Nuova Sessione" per ricominciare




















