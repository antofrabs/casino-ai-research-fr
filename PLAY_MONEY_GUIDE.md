# 🆓 Guida ai Siti Blackjack con Soldi Falsi (Play Money)

## 🎯 Cos'è Play Money?

I siti **Play Money** sono siti di blackjack online che usano **solo soldi virtuali/falsi**. Sono perfetti per:

- ✅ Testare l'AI senza rischi
- ✅ Imparare le strategie
- ✅ Praticare il conteggio carte
- ✅ Nessun bisogno di registrazione o login
- ✅ Gratuiti al 100%

## 🚀 Come Usarli

### 1. Avvia l'Interfaccia Web

```bash
python3 src/main.py
# Scegli opzione 1 (Web Interface)
```

### 2. STEP 1: Selezione Sito

Nell'interfaccia web, vai al tab **"🆓 Blackjack Play Money"**

Troverai una lista di siti preconfigurati:

- **247 Blackjack** - https://www.247blackjack.com
- **Blackjack.org** - https://www.blackjack.org
- **Casino.org Blackjack** - https://www.casino.org/blackjack/
- **CardGames.io** - https://cardgames.io/blackjack/
- **World of Card Games** - https://worldofcardgames.com/blackjack

Clicca su **"▶️ Usa"** accanto al sito che preferisci.

### 3. STEP 2: Credenziali

**NON sono necessarie credenziali!**

Vedrai un pulsante **"▶️ Continua senza Login"** - cliccalo per procedere.

### 4. STEP 3: Selezione Gioco

Scegli **Blackjack** (già selezionato per i siti play money).

### 5. STEP 4: Configurazione AI

Configura i parametri dell'AI:
- Bankroll iniziale (virtuale)
- Rischio per mano
- Stop-loss / Stop-win
- Conteggio carte

### 6. STEP 5: Auto-Pilota

Clicca **"🌐 Avvia Browser e Gioca"**

Il browser si aprirà automaticamente sul sito play money e l'AI inizierà a giocare!

## 🎮 Cosa Vedrai

- ✅ Browser aperto con il gioco di blackjack
- ✅ L'AI gioca automaticamente
- ✅ Screenshot in tempo reale nell'interfaccia web
- ✅ Metriche aggiornate (mani giocate, profitto virtuale, conteggio carte)
- ✅ Grafici del progresso

## ⚙️ Configurazione Siti

I selettori CSS per i siti play money sono configurati in:

`config/sites/play_money_sites.yaml`

Se un sito non funziona, potresti dover aggiustare i selettori CSS per quel sito specifico.

## 🔧 Aggiungere Nuovi Siti Play Money

Per aggiungere un nuovo sito, modifica `config/sites/play_money_sites.yaml`:

```yaml
sites:
  - name: "Nome Sito"
    url: "https://url-del-sito.com"
    description: "Descrizione"
    requires_login: false
    play_money: true
    game_type: "blackjack"
    selectors:
      hit_button: ".hit, button.hit"
      stand_button: ".stand, button.stand"
      # ... altri selettori
```

## 💡 Vantaggi Play Money

1. **Zero Rischi** - Nessun denaro reale coinvolto
2. **Nessuna Registrazione** - Inizia subito
3. **Test Illimitati** - Gioca quanto vuoi
4. **Perfetto per Test** - Ideale per sviluppare e testare l'AI
5. **Gratuito** - Completamente gratuito

## ⚠️ Note Importanti

- I selettori CSS potrebbero variare tra i siti
- Alcuni siti potrebbero avere pubblicità
- La struttura HTML dei siti può cambiare nel tempo
- Se un sito non funziona, prova un altro dalla lista

## 🎯 Siti Consigliati

### Per Principianti
- **247 Blackjack** - Interfaccia semplice
- **CardGames.io** - Design pulito

### Per Test Avanzati
- **Blackjack.org** - Molte opzioni
- **Casino.org** - Simulazione realistica

## 🚀 Inizia Subito!

1. Avvia: `python3 src/main.py`
2. Scegli: Tab "🆓 Blackjack Play Money"
3. Seleziona: Un sito dalla lista
4. Continua: Senza login
5. Gioca: L'AI giocherà automaticamente!

---

**Buon divertimento con i soldi virtuali! 🎰🆓**


















