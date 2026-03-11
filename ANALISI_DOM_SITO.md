# 🔍 Analisi DOM del Sito - Studio Struttura Elementi

## ✅ Funzionalità Implementata

Il sistema ora **analizza automaticamente il DOM del sito** prima di giocare per capire come sono strutturati gli elementi e usa selettori specifici per quel sito.

## 🎯 Come Funziona

### 1. **Analisi Automatica**
Quando entri nel gioco, il sistema:
1. **Attende il caricamento completo** della pagina
2. **Scansiona il DOM** per trovare elementi del gioco
3. **Identifica pattern** per chips, azioni, carte, aree betting, balance
4. **Genera selettori specifici** per quel sito
5. **Salva la configurazione** in un file YAML

### 2. **Cosa Analizza**

#### 🎲 **Chips**
- Cerca elementi con classi che contengono "chip" o "bet"
- Estrae valori da attributi (`data-value`, `data-chip`, `data-bet`)
- Identifica pattern nel testo ("10", "$10", "€10")
- Raggruppa per valore e trova il selettore migliore

#### 🎮 **Azioni (Hit, Stand, Double, Split)**
- Cerca pulsanti con testo corrispondente
- Verifica attributi (`data-action`, `aria-label`, `title`)
- Identifica classi comuni per ogni azione
- Trova il selettore più affidabile

#### 🎴 **Carte**
- Cerca elementi con classi che contengono "card"
- Identifica pattern di valori (A, K, Q, J, numeri)
- Estrae attributi (`data-card`, `data-suit`, `data-value`)

#### 🎯 **Aree Betting**
- Cerca canvas (molti giochi usano canvas)
- Identifica div con classi comuni (`.betting-area`, `.bet-area`, ecc.)
- Verifica dimensioni minime (almeno 50x50 pixel)

#### 💰 **Balance**
- Cerca elementi con classi che contengono "balance", "money", "credit"
- Identifica pattern numerici con simboli ($, €)
- Estrae il selettore più specifico

### 3. **Generazione Configurazione**

Il sistema genera automaticamente un file YAML con selettori specifici:

```yaml
url: https://example-casino.com
selectors:
  chip_10: ".chip-10"
  chip_25: ".chip-25"
  chip_50: "#bet-chip-50"
  chip_100: "[data-value='100']"
  chip_500: ".betting-chip-500"
  hit_button: "#hit-btn"
  stand_button: ".stand-button"
  double_button: "[data-action='double']"
  split_button: "button:has-text('Split')"
  betting_area: "canvas"
  balance: "#user-balance"
```

### 4. **Uso Automatico**

Durante il gioco, il sistema:
1. **Priorità 1**: Usa selettori dall'analisi del sito
2. **Priorità 2**: Usa selettori standard se l'analisi non ha trovato nulla
3. **Fallback**: Usa metodi generici se necessario

## 📊 Dettagli Tecnici

### Algoritmo di Analisi

1. **Scansione DOM Completa**
   - Esegue JavaScript nel browser per scansionare tutti gli elementi
   - Filtra solo elementi visibili (`offsetParent !== null`)
   - Verifica dimensioni minime per evitare elementi nascosti

2. **Raggruppamento Intelligente**
   - Raggruppa elementi simili per tipo
   - Estrae valori comuni (chip values, action types)
   - Identifica pattern ricorrenti

3. **Selezione Selettore Migliore**
   - **ID unico**: Preferito se presente e unico
   - **Classe comune**: Se presente in almeno 50% degli esempi
   - **Fallback**: Usa il primo selettore trovato

4. **Calcolo Confidence**
   - Base: 0.5
   - +0.2 se ci sono 3+ esempi
   - +0.2 se hanno ID unico
   - +0.1 se hanno classi comuni
   - Max: 1.0

### File Salvati

L'analisi viene salvata in:
```
config/sites/{sito}_analyzed.yaml
```

Esempio: `config/sites/www_247blackjack_com_analyzed.yaml`

## 🚀 Vantaggi

- ✅ **Adattamento automatico**: Si adatta a ogni sito senza configurazione manuale
- ✅ **Selettori specifici**: Usa i selettori migliori per quel sito
- ✅ **Meno errori**: Riconosce elementi anche con strutture non standard
- ✅ **Configurazione persistente**: Salva l'analisi per usi futuri
- ✅ **Confidence score**: Indica quanto è affidabile ogni selettore

## 💡 Esempio di Output

```
🔍 ANALISI DOM DEL SITO - Studio struttura elementi
======================================================================
   🎲 Analizzando chips...
      ✅ Chip $10 trovato: .chip-10 (confidence: 0.90)
      ✅ Chip $25 trovato: [data-value='25'] (confidence: 0.85)
      ✅ Chip $50 trovato: #bet-chip-50 (confidence: 0.95)
   🎮 Analizzando azioni...
      ✅ Azione 'hit' trovata: #hit-btn (confidence: 0.90)
      ✅ Azione 'stand' trovata: .stand-button (confidence: 0.85)
   🎴 Analizzando carte...
      ✅ Carte trovate: .playing-card (confidence: 0.75)
   🎯 Analizzando aree betting...
      ✅ Canvas betting trovato (index: 0)
   💰 Analizzando balance...
      ✅ Balance trovato: #user-balance (confidence: 0.90)
💾 Configurazione salvata in: config/sites/www_247blackjack_com_analyzed.yaml
======================================================================
```

## 🔧 Quando Viene Eseguita

L'analisi viene eseguita automaticamente:
- **Dopo il click su "Play"** quando entri nel gioco
- **Dopo la navigazione** al tavolo di gioco
- **Prima di iniziare a giocare** per avere selettori ottimali

## 📝 Note

- L'analisi richiede 2-5 secondi (dipende dalla complessità del sito)
- I selettori analizzati hanno sempre priorità sui selettori standard
- Se l'analisi non trova elementi, usa i selettori standard come fallback
- La configurazione viene salvata e riutilizzata nelle sessioni future

---

**Il sistema ora studia automaticamente ogni sito prima di giocare! 🔍**
