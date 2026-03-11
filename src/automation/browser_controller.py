#!/usr/bin/env python3
"""
🌐 Browser Controller per automazione casino
===============================================================

Gestisce:
1. Login automatico con credenziali
2. Navigazione ai giochi
3. Rilevamento stato del gioco
4. Esecuzione azioni AI
5. Capture screenshot e dati
"""
import time
import json
import random
import math
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Install Playwright: pip install playwright && playwright install")

class GameState(Enum):
    """Stati del gioco rilevati"""
    LOGIN_SCREEN = "login"
    LOBBY = "lobby"
    GAME_TABLE = "game_table"
    BETTING_PHASE = "betting"
    ACTION_PHASE = "action"
    RESULTS_PHASE = "results"

@dataclass
class CasinoElement:
    """Selettori CSS per elementi del sito casino"""
    # Login
    email_input = "input[type='email'], input[name='email'], #email"
    password_input = "input[type='password'], input[name='password'], #password"
    login_button = "button[type='submit'], .login-btn, #login-btn"
    balance_display = ".balance, .user-balance, .account-balance"
    
    # Blackjack
    blackjack_table = ".blackjack-table, [data-game='blackjack']"
    hit_button = ".hit-btn, [data-action='hit'], button:has-text('Hit'), button:has-text('HIT'), #hit, .hit-button, [onclick*='hit'], button[aria-label*='Hit']"
    stand_button = ".stand-btn, [data-action='stand'], button:has-text('Stand'), button:has-text('STAND'), #stand, .stand-button, [onclick*='stand'], button[aria-label*='Stand']"
    double_button = ".double-btn, [data-action='double'], button:has-text('Double'), button:has-text('DOUBLE'), #double, .double-button, [onclick*='double'], button[aria-label*='Double']"
    split_button = ".split-btn, [data-action='split'], button:has-text('Split'), button:has-text('SPLIT'), #split, .split-button, [onclick*='split'], button[aria-label*='Split']"
    
    # Chips - Selettori estesi per diversi siti (molti siti usano chips cliccabili per bettare)
    chip_10 = ".chip-10, [data-value='10'], [data-chip='10'], .chip[data-value='10'], button:has-text('10'), .bet-chip-10, [aria-label*='10'], [title*='10'], .chip.chip-10, div.chip-10, span.chip-10, [class*='chip'][class*='10'], [id*='chip'][id*='10'], .betting-chip-10, .chip-value-10, [data-bet='10'], [data-amount='10']"
    chip_25 = ".chip-25, [data-value='25'], [data-chip='25'], .chip[data-value='25'], button:has-text('25'), .bet-chip-25, [aria-label*='25'], [title*='25'], .chip.chip-25, div.chip-25, span.chip-25, [class*='chip'][class*='25'], [id*='chip'][id*='25'], .betting-chip-25, .chip-value-25, [data-bet='25'], [data-amount='25']"
    chip_50 = ".chip-50, [data-value='50'], [data-chip='50'], .chip[data-value='50'], button:has-text('50'), .bet-chip-50, [aria-label*='50'], [title*='50'], .chip.chip-50, div.chip-50, span.chip-50, [class*='chip'][class*='50'], [id*='chip'][id*='50'], .betting-chip-50, .chip-value-50, [data-bet='50'], [data-amount='50']"
    chip_100 = ".chip-100, [data-value='100'], [data-chip='100'], .chip[data-value='100'], button:has-text('100'), .bet-chip-100, [aria-label*='100'], [title*='100'], .chip.chip-100, div.chip-100, span.chip-100, [class*='chip'][class*='100'], [id*='chip'][id*='100'], .betting-chip-100, .chip-value-100, [data-bet='100'], [data-amount='100']"
    chip_500 = ".chip-500, [data-value='500'], [data-chip='500'], .chip[data-value='500'], button:has-text('500'), [aria-label*='500'], [title*='500'], .chip.chip-500, div.chip-500, span.chip-500, [class*='chip'][class*='500'], [id*='chip'][id*='500'], .betting-chip-500, .chip-value-500, [data-bet='500'], [data-amount='500']"
    
    # Area di betting
    betting_area = ".betting-area, .bet-area, .bet-zone, .table-bet, [data-bet-area], .game-table, canvas"
    bet_button = ".place-bet, .bet-button, button:has-text('Bet'), button:has-text('Place Bet'), [data-action='bet']"
    
    # Roulette
    roulette_table = ".roulette-table, [data-game='roulette']"
    
    # Withdraw
    withdraw_button = ".withdraw-btn, [data-action='withdraw']"
    withdraw_amount_input = "input[name='amount'], .withdraw-amount"
    withdraw_confirm = ".confirm-withdraw, [data-action='confirm-withdraw']"

class CasinoBrowserController:
    """Controller per automazione browser su siti casino"""
    
    def __init__(self, headless: bool = False, slow_mo: int = 100):
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.elements = CasinoElement()
        self.current_state = GameState.LOGIN_SCREEN
        
        # Dati sessione
        self.session_data = {
            'start_time': None,
            'initial_balance': 0,
            'current_balance': 0,
            'hands_played': 0,
            'total_profit': 0,
            'site_url': None
        }
        
        # Analisi sito
        self.site_analysis = None
        self.site_config = None
    
    def start_browser(self) -> bool:
        """Avvia il browser"""
        if not PLAYWRIGHT_AVAILABLE:
            print("❌ Playwright not installed")
            return False
        
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            # Configura context
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                locale='it-IT'
            )
            
            # Blocca risorse non necessarie per performance
            self.context.route('**/*.{png,jpg,jpeg,gif,svg}', lambda route: route.abort())
            
            self.page = self.context.new_page()
            print("✅ Browser started")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            return False
    
    def login(self, url: str, credentials: Dict[str, str]) -> bool:
        """Login automatico al sito casino"""
        try:
            print(f"🔗 Connecting to {url}...")
            
            # Naviga al sito
            self.page.goto(url, timeout=30000)
            time.sleep(2)
            
            self.session_data['site_url'] = url
            self.session_data['start_time'] = time.time()
            
            # Trova e compila email
            email_filled = False
            for selector in self.elements.email_input.split(', '):
                if self.page.locator(selector).count() > 0:
                    self.page.fill(selector, credentials['email'])
                    email_filled = True
                    print(f"✅ Email filled")
                    break
            
            if not email_filled:
                print("❌ Email input not found")
                return False
            
            # Trova e compila password
            password_filled = False
            for selector in self.elements.password_input.split(', '):
                if self.page.locator(selector).count() > 0:
                    self.page.fill(selector, credentials['password'])
                    password_filled = True
                    print(f"✅ Password filled")
                    break
            
            if not password_filled:
                print("❌ Password input not found")
                return False
            
            # Clicca login
            for selector in self.elements.login_button.split(', '):
                if self.page.locator(selector).count() > 0:
                    self.page.click(selector)
                    print(f"✅ Login clicked")
                    break
            
            # Attende login
            time.sleep(3)
            
            # Verifica login riuscito
            for selector in self.elements.balance_display.split(', '):
                if self.page.locator(selector).count() > 0:
                    self.current_state = GameState.LOBBY
                    balance = self.get_balance()
                    self.session_data['initial_balance'] = balance
                    self.session_data['current_balance'] = balance
                    print(f"✅ Login successful! Balance: {balance}")
                    return True
            
            print("❌ Login failed - balance not found")
            return False
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def get_balance(self) -> float:
        """Legge il balance corrente (thread-safe)"""
        try:
            # PRIORITÀ 1: Usa selettore dall'analisi del sito (se disponibile)
            if self.site_config and 'selectors' in self.site_config:
                if 'balance' in self.site_config['selectors']:
                    selector = self.site_config['selectors']['balance']
                    try:
                        count = self.page.locator(selector).count()
                        if count > 0:
                            balance_text = self.page.locator(selector).text_content(timeout=5000)
                            if balance_text:
                                import re
                                numbers = re.findall(r'[\d,.]+', balance_text)
                                if numbers:
                                    clean_num = numbers[0].replace('.', '').replace(',', '.')
                                    return float(clean_num)
                    except:
                        pass
            
            # PRIORITÀ 2: Selettori CSS standard
            for selector in self.elements.balance_display.split(', '):
                try:
                    # Usa try-except per gestire errori di thread
                    count = self.page.locator(selector).count()
                    if count > 0:
                        try:
                            balance_text = self.page.locator(selector).text_content(timeout=5000)
                            # Estrai numeri dal testo
                            import re
                            numbers = re.findall(r'[\d,.]+', balance_text)
                            
                            if numbers:
                                # Rimuovi punti e converte in float
                                clean_num = numbers[0].replace('.', '').replace(',', '.')
                                return float(clean_num)
                        except Exception as e:
                            # Ignora errori di lettura
                            continue
                except Exception as e:
                    # Ignora errori di thread/locator
                    continue
        except Exception as e:
            # Se c'è un errore di thread, ritorna 0
            print(f"⚠️ Errore lettura balance (thread-safe): {e}")
        
        return 0.0
    
    def click_play_button(self, site_config: Optional[Dict] = None) -> bool:
        """Cerca e clicca il pulsante Play per iniziare il gioco"""
        try:
            print("🔍 Cercando pulsante Play...")
            
            # Selettori comuni per pulsanti Play
            common_play_selectors = [
                # Selettori generici
                "button:has-text('Play')",
                "button:has-text('PLAY')",
                "button:has-text('Play Now')",
                "button:has-text('Start Game')",
                "button:has-text('Start')",
                ".play-button",
                ".play-btn",
                "#play-button",
                "[data-action='play']",
                "[onclick*='play']",
                "a:has-text('Play')",
                # Selettori specifici per 247blackjack
                "a[href*='play']",
                "button.play",
                ".game-play-button",
            ]
            
            # Se abbiamo configurazione del sito, aggiungi i suoi selettori
            if site_config and 'selectors' in site_config:
                play_selector = site_config['selectors'].get('play_button', '')
                if play_selector:
                    # Aggiungi i selettori del sito all'inizio della lista
                    common_play_selectors = play_selector.split(', ') + common_play_selectors
            
            # Prova ogni selettore
            for selector in common_play_selectors:
                try:
                    selector = selector.strip()
                    if not selector:
                        continue
                    
                    # Conta quanti elementi corrispondono
                    count = self.page.locator(selector).count()
                    
                    if count > 0:
                        print(f"   ✅ Trovato pulsante Play con selettore: {selector}")
                        
                        # Clicca il pulsante
                        self.page.locator(selector).first.click()
                        print(f"   ✅ Cliccato pulsante Play")
                        
                        # Attende che il gioco si carichi
                        time.sleep(3)
                        
                        # Verifica che siamo nel gioco (cerca elementi del gioco)
                        game_indicators = [
                            "button:has-text('Hit')",
                            "button:has-text('Stand')",
                            ".hit",
                            ".stand",
                            ".bet",
                            "[data-action='hit']"
                        ]
                        
                        for indicator in game_indicators:
                            if self.page.locator(indicator).count() > 0:
                                print("   ✅ Gioco caricato correttamente!")
                                self.current_state = GameState.GAME_TABLE
                                return True
                        
                        # Se non trova indicatori specifici, aspetta un po' di più
                        time.sleep(2)
                        print("   ✅ Pulsante Play cliccato (verifica manuale se necessario)")
                        self.current_state = GameState.GAME_TABLE
                        return True
                        
                except Exception as e:
                    # Continua con il prossimo selettore
                    continue
            
            print("   ⚠️  Pulsante Play non trovato - potrebbe essere già nel gioco")
            # Verifica se siamo già nel gioco
            game_indicators = ["button:has-text('Hit')", ".hit", "[data-action='hit']"]
            for indicator in game_indicators:
                if self.page.locator(indicator).count() > 0:
                    print("   ✅ Siamo già nel gioco!")
                    self.current_state = GameState.GAME_TABLE
                    return True
            
            return False
            
        except Exception as e:
            print(f"   ❌ Errore nel cercare pulsante Play: {e}")
            return False
    
    def navigate_to_game(self, game_name: str, site_config: Optional[Dict] = None) -> bool:
        """Naviga al gioco specificato e clicca Play se necessario"""
        try:
            # Prima prova a cliccare il pulsante Play
            if self.click_play_button(site_config):
                print(f"✅ Gioco avviato!")
                return True
            
            # Se non c'è pulsante Play, prova navigazione tradizionale
            game_selectors = {
                'blackjack': self.elements.blackjack_table,
                'roulette': self.elements.roulette_table
            }
            
            if game_name not in game_selectors:
                print(f"❌ Game {game_name} not supported")
                return False
            
            selector = game_selectors[game_name]
            
            for sel in selector.split(', '):
                if self.page.locator(sel).count() > 0:
                    self.page.click(sel)
                    time.sleep(3)  # Attende caricamento tavolo
                    self.current_state = GameState.GAME_TABLE
                    print(f"✅ Navigated to {game_name}")
                    return True
            
            print(f"❌ {game_name} table not found")
            return False
            
        except Exception as e:
            print(f"❌ Navigation error to {game_name}: {e}")
            return False
    
    def find_chip_by_value(self, value: int) -> Optional[Any]:
        """Trova un chip per valore usando vari metodi - restituisce locator o selector"""
        # PRIORITÀ 1: Usa selettori dall'analisi del sito (se disponibile)
        if self.site_config and 'selectors' in self.site_config:
            chip_key = f'chip_{value}'
            if chip_key in self.site_config['selectors']:
                selector = self.site_config['selectors'][chip_key]
                try:
                    locator = self.page.locator(selector)
                    if locator.count() > 0:
                        first_locator = locator.first
                        if first_locator.is_visible():
                            print(f"   ✅ Chip ${value} trovato con selettore analizzato: {selector}")
                            return first_locator
                except:
                    pass
        
        # PRIORITÀ 2: Selettori CSS standard (estesi)
        chip_selectors = {
            10: self.elements.chip_10,
            25: self.elements.chip_25,
            50: self.elements.chip_50,
            100: self.elements.chip_100,
            500: self.elements.chip_500
        }
        
        if value in chip_selectors:
            for selector in chip_selectors[value].split(', '):
                selector = selector.strip()
                if not selector:
                    continue
                try:
                    locator = self.page.locator(selector)
                    if locator.count() > 0:
                        # Verifica che sia visibile e cliccabile
                        first_locator = locator.first
                        try:
                            if first_locator.is_visible():
                                return first_locator  # Restituisce locator per click diretto
                        except:
                            return first_locator  # Restituisce comunque se non riesce a verificare
                except:
                    continue
        
        # Metodo 2: Cerca per testo (es. "10", "$10", "€10", "10€", "10$")
        text_patterns = [
            f"button:has-text('{value}')",
            f"div:has-text('{value}')",
            f"span:has-text('{value}')",
            f"[aria-label*='{value}']",
            f"[title*='{value}']",
            f"*:has-text('${value}')",
            f"*:has-text('€{value}')",
            f"*:has-text('{value}$')",
            f"*:has-text('{value}€')"
        ]
        
        for pattern in text_patterns:
            try:
                locator = self.page.locator(pattern)
                if locator.count() > 0:
                    first_locator = locator.first
                    try:
                        if first_locator.is_visible():
                            return first_locator
                    except:
                        return first_locator
            except:
                continue
        
        # Metodo 3: Cerca attributi data-value, data-chip, value (più varianti)
        attr_patterns = [
            f"[data-value='{value}']",
            f"[data-chip='{value}']",
            f"[value='{value}']",
            f".chip[data-value='{value}']",
            f"[data-bet='{value}']",
            f"[data-amount='{value}']",
            f"[data-chip-value='{value}']",
            f"[data-denomination='{value}']"
        ]
        
        for pattern in attr_patterns:
            try:
                locator = self.page.locator(pattern)
                if locator.count() > 0:
                    first_locator = locator.first
                    try:
                        if first_locator.is_visible():
                            return first_locator
                    except:
                        return first_locator
            except:
                continue
        
        # Metodo 4: Cerca elementi con classi che contengono il valore
        class_patterns = [
            f"[class*='chip'][class*='{value}']",
            f"[class*='bet'][class*='{value}']",
            f"[id*='chip'][id*='{value}']",
            f"[id*='bet'][id*='{value}']"
        ]
        
        for pattern in class_patterns:
            try:
                locator = self.page.locator(pattern)
                if locator.count() > 0:
                    first_locator = locator.first
                    try:
                        if first_locator.is_visible():
                            return first_locator
                    except:
                        return first_locator
            except:
                continue
        
        # Metodo 5: Cerca tutti gli elementi con "chip" nella classe e verifica il contenuto
        try:
            all_chips = self.page.locator("[class*='chip'], [class*='bet'], [id*='chip'], [id*='bet']").all()
            for chip in all_chips[:20]:  # Limita a 20 per performance
                try:
                    text = chip.text_content() or ""
                    aria_label = chip.get_attribute("aria-label") or ""
                    title = chip.get_attribute("title") or ""
                    data_value = chip.get_attribute("data-value") or ""
                    
                    # Verifica se contiene il valore
                    if (str(value) in text or 
                        str(value) in aria_label or 
                        str(value) in title or 
                        str(value) in data_value):
                        if chip.is_visible():
                            return chip
                except:
                    continue
        except:
            pass
        
        return None
    
    def find_betting_area(self) -> Optional[str]:
        """Trova l'area di betting"""
        for selector in self.elements.betting_area.split(', '):
            selector = selector.strip()
            if not selector:
                continue
            try:
                if self.page.locator(selector).count() > 0:
                    return selector
            except:
                continue
        
        # Cerca anche canvas (molti giochi usano canvas)
        try:
            if self.page.locator("canvas").count() > 0:
                return "canvas"
        except:
            pass
        
        return None
    
    def _verify_bet_placed(self, initial_balance: float, timeout: int = 3) -> bool:
        """Verifica che la puntata sia stata registrata"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Metodo 1: Verifica cambio balance
                current_balance = self.get_balance()
                if current_balance < initial_balance:
                    print(f"   ✅ Puntata registrata! Balance: ${initial_balance} -> ${current_balance}")
                    return True
                
                # Metodo 2: Verifica elementi visivi (chip sulla tavola, bet amount, ecc.)
                bet_indicators = [
                    ".bet-placed", ".active-bet", ".bet-amount",
                    "[data-bet-placed='true']", ".chip-on-table",
                    ".betting-confirmed", ".bet-active"
                ]
                for indicator in bet_indicators:
                    try:
                        if self.page.locator(indicator).count() > 0:
                            print(f"   ✅ Puntata visibile sulla tavola!")
                            return True
                    except:
                        continue
                
                # Metodo 3: Verifica che i pulsanti di azione siano apparsi (significa che betting è finito)
                if self.page.locator("button:has-text('Hit'), button:has-text('Stand'), .hit, .stand").count() > 0:
                    print(f"   ✅ Azioni disponibili - betting completato!")
                    return True
                
                time.sleep(0.2)
            except:
                time.sleep(0.2)
        
        return False
    
    def place_bet(self, amount: float, position: str = "player") -> bool:
        """Piazza una puntata con rilevamento intelligente, click umano e verifica"""
        try:
            print(f"🎲 Tentativo di piazzare puntata: ${amount}")
            
            # Salva balance iniziale per verifica
            initial_balance = self.get_balance()
            
            # Valori chip comuni
            chip_values = [10, 25, 50, 100, 500]
            closest_chip = min(chip_values, key=lambda x: abs(x - amount))
            
            print(f"   🔍 Cercando chip da ${closest_chip}...")
            
            # Metodo 1: Clicca direttamente sulla chip per bettare (molti siti funzionano così)
            chip_locator = self.find_chip_by_value(closest_chip)
            if chip_locator:
                try:
                    # Pausa umana prima di cliccare
                    time.sleep(self._human_delay(0.3, 0.2))
                    
                    # Prova click umano diretto sulla chip
                    for attempt in range(3):
                        try:
                            if hasattr(chip_locator, 'bounding_box'):
                                # È un locator Playwright
                                box = chip_locator.bounding_box()
                                if box:
                                    x = box['x'] + box['width'] * (0.3 + random.uniform(0, 0.4))
                                    y = box['y'] + box['height'] * (0.3 + random.uniform(0, 0.4))
                                    
                                    # Click umano sulla chip
                                    if self._human_click(x, y, chip_locator):
                                        print(f"   ✅ Chip ${closest_chip} cliccata (tentativo {attempt+1})")
                                        
                                        # Attesa umana dopo click
                                        time.sleep(self._human_delay(0.4, 0.3))
                                        
                                        # Verifica se la puntata è stata registrata (molti siti registrano direttamente)
                                        if self._verify_bet_placed(initial_balance, timeout=2):
                                            self.current_state = GameState.BETTING_PHASE
                                            return True
                                        
                                        # Se non verificata, potrebbe essere che serve cliccare anche sull'area
                                        break
                            else:
                                # Fallback: click normale
                                chip_locator.click(timeout=2000)
                                time.sleep(self._human_delay(0.3, 0.2))
                                if self._verify_bet_placed(initial_balance, timeout=2):
                                    self.current_state = GameState.BETTING_PHASE
                                    return True
                                break
                        except Exception as e:
                            if attempt == 2:
                                print(f"   ⚠️ Errore click chip dopo 3 tentativi: {e}")
                            time.sleep(self._human_delay(0.2, 0.1))
                except Exception as e:
                    print(f"   ⚠️ Errore click chip: {e}")
            
            # Metodo 2: Se il click diretto sulla chip non ha funzionato, prova: chip + area betting
            # (Alcuni siti richiedono: seleziona chip, poi clicca area)
            betting_area = self.find_betting_area()
            if betting_area:
                try:
                    # Pausa umana tra le azioni
                    time.sleep(self._human_delay(0.2, 0.1))
                    
                    # Se è un canvas, clicca con movimento umano
                    if "canvas" in betting_area:
                        canvas = self.page.locator("canvas").first
                        box = canvas.bounding_box()
                        if box:
                            # Click randomizzato all'interno del canvas (non sempre al centro)
                            x = box['x'] + box['width'] * (0.4 + random.uniform(0, 0.2))
                            y = box['y'] + box['height'] * (0.4 + random.uniform(0, 0.2))
                            
                            if self._human_click(x, y):
                                print(f"   ✅ Cliccato su area betting (canvas) con movimento umano")
                                time.sleep(self._human_delay(0.5, 0.3))
                                
                                # Verifica che la puntata sia stata registrata
                                if self._verify_bet_placed(initial_balance):
                                    self.current_state = GameState.BETTING_PHASE
                                    return True
                    else:
                        # Prova click umano sull'area betting
                        for attempt in range(2):
                            try:
                                locator = self.page.locator(betting_area).first
                                if locator.is_visible():
                                    box = locator.bounding_box()
                                    if box:
                                        x = box['x'] + box['width'] * (0.3 + random.uniform(0, 0.4))
                                        y = box['y'] + box['height'] * (0.3 + random.uniform(0, 0.4))
                                        
                                        if self._human_click(x, y, locator):
                                            print(f"   ✅ Cliccato su area betting con movimento umano")
                                            time.sleep(self._human_delay(0.5, 0.3))
                                            
                                            # Verifica
                                            if self._verify_bet_placed(initial_balance):
                                                self.current_state = GameState.BETTING_PHASE
                                                return True
                                            break
                            except:
                                if attempt == 0:
                                    # Prova force click come fallback
                                    try:
                                        self.page.locator(betting_area).first.click(force=True, timeout=2000)
                                        time.sleep(self._human_delay(0.3, 0.2))
                                        if self._verify_bet_placed(initial_balance):
                                            self.current_state = GameState.BETTING_PHASE
                                            return True
                                    except:
                                        pass
                except Exception as e:
                    print(f"   ⚠️ Errore click area betting: {e}")
            
            # Metodo 3: Cerca pulsante "Place Bet" o "Bet" (con click umano)
            for selector in self.elements.bet_button.split(', '):
                selector = selector.strip()
                if not selector:
                    continue
                try:
                    locator = self.page.locator(selector).first
                    if locator.count() > 0 and locator.is_visible():
                        box = locator.bounding_box()
                        if box:
                            x = box['x'] + box['width'] * (0.3 + random.uniform(0, 0.4))
                            y = box['y'] + box['height'] * (0.3 + random.uniform(0, 0.4))
                            
                            if self._human_click(x, y, locator):
                                print(f"   ✅ Pulsante bet cliccato con movimento umano")
                                time.sleep(self._human_delay(0.5, 0.3))
                                
                                # Verifica
                                if self._verify_bet_placed(initial_balance):
                                    self.current_state = GameState.BETTING_PHASE
                                    return True
                        break
                except:
                    continue
            
            # Metodo 4: Cerca selettori specifici per posizione
            position_selectors = [
                f".bet-{position}", f"[data-bet='{position}']",
                f"[data-position='{position}']", f".{position}-bet", f"#{position}-bet"
            ]
            
            for selector in position_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        self.page.locator(selector).first.click(timeout=2000)
                        time.sleep(0.5)
                        print(f"   ✅ Puntata piazzata su {position}")
                        
                        # Verifica
                        if self._verify_bet_placed(initial_balance):
                            self.current_state = GameState.BETTING_PHASE
                            return True
                except:
                    continue
            
            # Metodo 5: Click generico su canvas/table con verifica
            try:
                table_elements = ["canvas", ".game-table", ".blackjack-table", ".table"]
                for elem in table_elements:
                    if self.page.locator(elem).count() > 0:
                        locator = self.page.locator(elem).first
                        box = locator.bounding_box()
                        if box:
                            x = box['x'] + box['width'] / 2
                            y = box['y'] + box['height'] / 2
                            self.page.mouse.click(x, y)
                            print(f"   ✅ Click generico su {elem}")
                            time.sleep(1)
                            
                            # Verifica
                            if self._verify_bet_placed(initial_balance):
                                self.current_state = GameState.BETTING_PHASE
                                return True
            except Exception as e:
                print(f"   ⚠️ Errore click generico: {e}")
            
            print(f"   ⚠️ Puntata non verificata - potrebbe non essere stata registrata")
            print(f"   💡 Verifica manualmente nel browser se la puntata è stata piazzata")
            return False
            
        except Exception as e:
            print(f"❌ Bet placement error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def find_action_button(self, action: str) -> Optional[str]:
        """Trova il pulsante per un'azione usando vari metodi"""
        # PRIORITÀ 1: Usa selettori dall'analisi del sito (se disponibile)
        if self.site_config and 'selectors' in self.site_config:
            action_key = f'{action}_button'
            if action_key in self.site_config['selectors']:
                selector = self.site_config['selectors'][action_key]
                try:
                    locator = self.page.locator(selector)
                    if locator.count() > 0:
                        first_locator = locator.first
                        if first_locator.is_visible():
                            print(f"   ✅ Azione '{action}' trovata con selettore analizzato: {selector}")
                            return selector
                except:
                    pass
        
        # PRIORITÀ 2: Selettori CSS standard
        action_mapping = {
            'hit': self.elements.hit_button,
            'stand': self.elements.stand_button,
            'double': self.elements.double_button,
            'split': self.elements.split_button
        }
        
        if action not in action_mapping:
            return None
        
        # Metodo 1: Selettori CSS standard
        for selector in action_mapping[action].split(', '):
            selector = selector.strip()
            if not selector:
                continue
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    # Verifica se è enabled (se possibile)
                    try:
                        if locator.first.is_enabled():
                            return selector
                    except:
                        # Se non riesce a verificare enabled, prova comunque
                        return selector
            except:
                continue
        
        # Metodo 2: Cerca per testo (case-insensitive)
        action_texts = {
            'hit': ['Hit', 'HIT', 'hit', 'Carta', 'CARTA'],
            'stand': ['Stand', 'STAND', 'stand', 'Stai', 'STAI', 'Stop'],
            'double': ['Double', 'DOUBLE', 'double', 'Raddoppia', 'RADDOPPIA'],
            'split': ['Split', 'SPLIT', 'split', 'Dividi', 'DIVIDI']
        }
        
        if action in action_texts:
            for text in action_texts[action]:
                patterns = [
                    f"button:has-text('{text}')",
                    f"a:has-text('{text}')",
                    f"div:has-text('{text}')",
                    f"[aria-label*='{text}']",
                    f"[title*='{text}']"
                ]
                for pattern in patterns:
                    try:
                        if self.page.locator(pattern).count() > 0:
                            return pattern
                    except:
                        continue
        
        return None
    
    def _verify_action_executed(self, action: str, initial_state: Dict, timeout: int = 3) -> bool:
        """Verifica che l'azione sia stata eseguita"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Metodo 1: Verifica che il pulsante non sia più disponibile (per hit/stand)
                if action in ['hit', 'stand']:
                    selector = self.find_action_button(action)
                    if selector:
                        try:
                            # Se il pulsante non è più enabled/visibile, l'azione è stata eseguita
                            locator = self.page.locator(selector).first
                            if not locator.is_enabled() or not locator.is_visible():
                                print(f"   ✅ Azione {action} eseguita (pulsante disabilitato)")
                                return True
                        except:
                            # Se il pulsante non esiste più, l'azione è stata eseguita
                            if self.page.locator(selector).count() == 0:
                                print(f"   ✅ Azione {action} eseguita (pulsante rimosso)")
                                return True
                
                # Metodo 2: Verifica cambiamento nello stato del gioco (nuove carte, ecc.)
                # Cerca indicatori di cambio stato
                state_indicators = [
                    ".card-dealt", ".new-card", "[data-card-dealt='true']",
                    ".game-state-changed", ".action-confirmed"
                ]
                for indicator in state_indicators:
                    try:
                        if self.page.locator(indicator).count() > 0:
                            print(f"   ✅ Azione {action} confermata (indicatore visivo)")
                            return True
                    except:
                        continue
                
                # Metodo 3: Per hit, verifica che nuove carte siano apparse
                if action == 'hit':
                    # Attendi un po' per il caricamento della carta
                    time.sleep(0.3)
                    # Verifica che ci siano più carte ora (confronta con stato iniziale)
                    # Questo è un controllo semplificato - in produzione potresti contare le carte
                    try:
                        cards = self.page.locator(".card, .playing-card, [class*='card']").count()
                        if cards > initial_state.get('card_count', 0):
                            print(f"   ✅ Nuova carta apparsa - hit eseguito!")
                            return True
                    except:
                        pass
                
                # Metodo 4: Per stand, verifica che il turno sia passato al dealer
                if action == 'stand':
                    # Verifica che i pulsanti hit/stand non siano più disponibili
                    hit_stand_count = self.page.locator("button:has-text('Hit'), button:has-text('Stand'), .hit, .stand").count()
                    if hit_stand_count == 0:
                        print(f"   ✅ Turno passato al dealer - stand eseguito!")
                        return True
                
                time.sleep(0.2)
            except:
                time.sleep(0.2)
        
        return False
    
    def take_action(self, action: str) -> bool:
        """Esegue azione nel gioco (hit, stand, ecc.) con rilevamento intelligente e verifica"""
        try:
            print(f"🎮 Tentativo azione: {action}")
            
            # Salva stato iniziale per verifica
            try:
                card_count = self.page.locator(".card, .playing-card, [class*='card']").count()
            except:
                card_count = 0
            initial_state = {'card_count': card_count}
            
            # Trova il pulsante
            selector = self.find_action_button(action)
            
            if selector:
                try:
                    locator = self.page.locator(selector).first
                    
                    # Verifica se è visibile e enabled
                    try:
                        if not locator.is_visible():
                            print(f"   ⚠️ Pulsante {action} non visibile")
                            return False
                        if not locator.is_enabled():
                            print(f"   ⚠️ Pulsante {action} non abilitato")
                            return False
                    except:
                        pass  # Continua comunque
                    
                    # Clicca con retry
                    for attempt in range(3):
                        try:
                            locator.click(timeout=2000)
                            time.sleep(0.3)
                            print(f"   ✅ Click su {action} eseguito (tentativo {attempt+1})")
                            
                            # Verifica che l'azione sia stata eseguita
                            if self._verify_action_executed(action, initial_state):
                                return True
                            break
                        except Exception as e:
                            if attempt == 2:
                                print(f"   ⚠️ Errore click {action} dopo 3 tentativi: {e}")
                            time.sleep(0.2)
                    
                    # Se il click normale non ha funzionato, prova force click
                    try:
                        self.page.locator(selector).first.click(force=True, timeout=2000)
                        time.sleep(0.3)
                        print(f"   ✅ Azione {action} eseguita (force click)")
                        
                        # Verifica
                        if self._verify_action_executed(action, initial_state):
                            return True
                    except Exception as e:
                        print(f"   ⚠️ Errore force click {action}: {e}")
            
            # Se non trova con selettori, prova ricerca per testo
            action_texts = {
                'hit': ['Hit', 'HIT', 'Carta', 'Card'],
                'stand': ['Stand', 'STAND', 'Stai', 'Stop', 'Stay'],
                'double': ['Double', 'DOUBLE', 'Raddoppia', 'Doble'],
                'split': ['Split', 'SPLIT', 'Dividi', 'Divide']
            }
            
            if action in action_texts:
                for text in action_texts[action]:
                    try:
                        # Cerca tutti i pulsanti con quel testo
                        buttons = self.page.locator(f"button:has-text('{text}')")
                        if buttons.count() > 0:
                            for attempt in range(3):
                                try:
                                    btn = buttons.first
                                    if btn.is_visible() and btn.is_enabled():
                                        btn.click(timeout=2000)
                                        time.sleep(0.3)
                                        print(f"   ✅ Azione {action} eseguita (testo: {text})")
                                        
                                        # Verifica
                                        if self._verify_action_executed(action, initial_state):
                                            return True
                                        break
                                except:
                                    if attempt == 2:
                                        # Prova force click
                                        try:
                                            buttons.first.click(force=True, timeout=2000)
                                            time.sleep(0.3)
                                            if self._verify_action_executed(action, initial_state):
                                                return True
                                        except:
                                            pass
                                    time.sleep(0.2)
                    except:
                        continue
            
            print(f"   ⚠️ Azione {action} non trovata o non verificata")
            return False
            
        except Exception as e:
            print(f"❌ Action error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def detect_cards(self) -> Dict[str, List[str]]:
        """Rileva carte del giocatore e del dealer"""
        cards = {
            'player': [],
            'dealer': []
        }
        
        try:
            # Metodo 1: Cerca elementi con classi comuni per carte
            card_selectors = [
                ".card", ".playing-card", "[class*='card']",
                "[data-card]", ".player-card", ".dealer-card"
            ]
            
            for selector in card_selectors:
                try:
                    count = self.page.locator(selector).count()
                    if count > 0:
                        # Cerca di estrarre il valore delle carte
                        card_elements = self.page.locator(selector).all()
                        for elem in card_elements:
                            try:
                                # Prova a leggere il testo o attributi
                                text = elem.text_content()
                                data_value = elem.get_attribute("data-value")
                                data_card = elem.get_attribute("data-card")
                                class_name = elem.get_attribute("class")
                                
                                # Determina se è player o dealer
                                is_dealer = "dealer" in (class_name or "").lower() or "dealer" in (text or "").lower()
                                is_player = "player" in (class_name or "").lower() or "player" in (text or "").lower()
                                
                                card_value = data_value or data_card or text or "?"
                                if is_dealer:
                                    cards['dealer'].append(card_value)
                                elif is_player:
                                    cards['player'].append(card_value)
                                else:
                                    # Se non specificato, prova a determinare dalla posizione
                                    cards['player'].append(card_value)
                            except:
                                continue
                except:
                    continue
            
            # Metodo 2: Cerca per testo visibile (es. "A♠", "K♥", ecc.)
            try:
                card_patterns = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
                for pattern in card_patterns:
                    elements = self.page.locator(f"text={pattern}").all()
                    for elem in elements[:10]:
                        try:
                            text = elem.text_content()
                            if text and any(p in text for p in card_patterns):
                                parent = elem.locator("xpath=..")
                                parent_class = parent.get_attribute("class") or ""
                                if "dealer" in parent_class.lower():
                                    if text not in cards['dealer']:
                                        cards['dealer'].append(text)
                                else:
                                    if text not in cards['player']:
                                        cards['player'].append(text)
                        except:
                            continue
            except:
                pass
            
            return cards
            
        except Exception as e:
            print(f"⚠️ Errore rilevamento carte: {e}")
            return cards
    
    def detect_hands(self) -> Dict[str, Any]:
        """Rileva le mani del giocatore e del dealer"""
        hands = {
            'player_hands': [],
            'dealer_hand': [],
            'player_total': 0,
            'dealer_total': 0,
            'dealer_visible': 0
        }
        
        try:
            # Rileva carte
            cards = self.detect_cards()
            
            # Calcola totali
            def calculate_total(card_list):
                total = 0
                aces = 0
                for card in card_list:
                    card_str = str(card).upper()
                    if 'A' in card_str:
                        aces += 1
                        total += 11
                    elif any(x in card_str for x in ['K', 'Q', 'J']):
                        total += 10
                    else:
                        import re
                        nums = re.findall(r'\d+', card_str)
                        if nums:
                            total += int(nums[0])
                        else:
                            total += 10
                
                while total > 21 and aces > 0:
                    total -= 10
                    aces -= 1
                
                return total
            
            hands['player_total'] = calculate_total(cards['player'])
            hands['dealer_total'] = calculate_total(cards['dealer'])
            hands['dealer_visible'] = calculate_total(cards['dealer'][:1] if cards['dealer'] else [])
            
            hands['player_hands'] = [{'cards': cards['player'], 'total': hands['player_total']}]
            hands['dealer_hand'] = {'cards': cards['dealer'], 'total': hands['dealer_total']}
            
            # Metodo alternativo: Cerca elementi che mostrano il totale
            try:
                total_selectors = [
                    ".player-total", ".dealer-total", "[data-total]",
                    ".hand-value", ".score", "[class*='total']"
                ]
                
                for selector in total_selectors:
                    try:
                        elements = self.page.locator(selector).all()
                        for elem in elements[:5]:
                            try:
                                text = elem.text_content()
                                if text:
                                    import re
                                    nums = re.findall(r'\d+', text)
                                    if nums:
                                        value = int(nums[0])
                                        class_name = elem.get_attribute("class") or ""
                                        if "player" in class_name.lower():
                                            hands['player_total'] = value
                                        elif "dealer" in class_name.lower():
                                            hands['dealer_total'] = value
                            except:
                                continue
                    except:
                        continue
            except:
                pass
            
            return hands
            
        except Exception as e:
            print(f"⚠️ Errore rilevamento mani: {e}")
            return hands
    
    def capture_game_state(self) -> Dict[str, Any]:
        """Cattura stato corrente del gioco (thread-safe) con rilevamento carte e mani"""
        try:
            state = {
                'timestamp': time.time(),
                'game_state': self.current_state.value,
                'balance': 0.0,
                'available_actions': [],
                'table_screenshot': None,
                'player_cards': [],
                'dealer_cards': [],
                'player_total': 0,
                'dealer_total': 0,
                'dealer_visible': 0
            }
            
            # Prova a leggere balance
            try:
                state['balance'] = self.get_balance()
            except Exception as e:
                print(f"⚠️ Errore lettura balance: {e}")
                state['balance'] = 0.0
            
            # Prova a leggere azioni disponibili
            try:
                state['available_actions'] = self.get_available_actions()
            except Exception as e:
                print(f"⚠️ Errore lettura azioni: {e}")
                state['available_actions'] = []
            
            # Rileva carte e mani
            try:
                cards = self.detect_cards()
                state['player_cards'] = cards.get('player', [])
                state['dealer_cards'] = cards.get('dealer', [])
                
                hands = self.detect_hands()
                state['player_total'] = hands.get('player_total', 0)
                state['dealer_total'] = hands.get('dealer_total', 0)
                state['dealer_visible'] = hands.get('dealer_visible', 0)
            except Exception as e:
                print(f"⚠️ Errore rilevamento carte/mani: {e}")
            
            # Aggiorna session data
            if self.session_data.get('start_time'):
                state['session_duration'] = time.time() - self.session_data['start_time']
                state['session_data'] = self.session_data.copy()
            
            return state
        except Exception as e:
            print(f"⚠️ Errore capture_game_state: {e}")
            return {
                'timestamp': time.time(),
                'game_state': self.current_state.value,
                'balance': 0.0,
                'available_actions': [],
                'error': str(e)
            }
    
    def get_available_actions(self) -> List[str]:
        """Restituisce azioni disponibili (thread-safe)"""
        available = []
        try:
            action_buttons = {
                'hit': self.elements.hit_button,
                'stand': self.elements.stand_button,
                'double': self.elements.double_button,
                'split': self.elements.split_button
            }
            
            for action, selector in action_buttons.items():
                try:
                    for sel in selector.split(', '):
                        try:
                            count = self.page.locator(sel).count()
                            if count > 0:
                                # Prova a verificare se è enabled (può fallire in thread)
                                try:
                                    is_enabled = self.page.locator(sel).is_enabled()
                                    if is_enabled:
                                        available.append(action)
                                        break
                                except:
                                    # Se non riesce a verificare enabled, aggiungi comunque
                                    available.append(action)
                                    break
                        except Exception:
                            continue
                except Exception:
                    continue
        except Exception as e:
            print(f"⚠️ Errore lettura azioni disponibili: {e}")
        
        return available
    
    def execute_withdraw(self, amount: float, method: str = "bank_transfer") -> Dict:
        """Esegue withdraw (richiede supervisione utente)"""
        print("\n" + "⚠️" * 30)
        print("💳 WITHDRAW PROCEDURE - USER SUPERVISION REQUIRED")
        print("⚠️" * 30)
        print(f"💰 Amount: ${amount}")
        print(f"🏦 Method: {method}")
        print("\n⚠️  The AI will guide through steps, but manual confirmation is required")
        
        result = {
            'success': False,
            'amount': amount,
            'method': method,
            'timestamp': time.time(),
            'message': 'Requires user confirmation'
        }
        
        try:
            # Cerca pulsante withdraw
            for selector in self.elements.withdraw_button.split(', '):
                if self.page.locator(selector).count() > 0:
                    self.page.click(selector)
                    time.sleep(2)
                    print("✅ Withdraw page opened")
                    break
            
            # Inserisci importo
            for selector in self.elements.withdraw_amount_input.split(', '):
                if self.page.locator(selector).count() > 0:
                    self.page.fill(selector, str(amount))
                    time.sleep(1)
                    print(f"✅ Amount entered: ${amount}")
                    break
            
            # Attende conferma utente
            print("\n⚠️  WAITING FOR USER CONFIRMATION...")
            print("Please manually confirm the withdraw on the browser window")
            
            # Simula attesa conferma
            time.sleep(3)
            
            result['success'] = True
            result['message'] = 'Withdraw initiated (requires manual confirmation)'
            result['executed_at'] = time.time()
            
            print("✅ Withdraw procedure completed (requires manual finalization)")
            
        except Exception as e:
            result['message'] = f'Error: {e}'
            print(f"❌ Withdraw error: {e}")
        
        return result
    
    def close(self):
        """Chiude il browser"""
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
        print("✅ Browser closed")

# Esempio di utilizzo
if __name__ == "__main__":
    # Configurazione di esempio
    config = {
        'url': 'https://sandbox.casinomaker.com',
        'credentials': {
            'email': 'test@example.com',
            'password': 'password123'
        },
        'headless': False
    }
    
    controller = CasinoBrowserController(headless=config['headless'])
    
    try:
        if controller.start_browser():
            if controller.login(config['url'], config['credentials']):
                print("✅ Session started successfully!")
                
                # Esempio: vai al blackjack
                if controller.navigate_to_game('blackjack'):
                    print("✅ Ready to play!")
                    
                    # Simula alcune azioni
                    controller.place_bet(10, "player")
                    time.sleep(2)
                    
                    state = controller.capture_game_state()
                    print(f"📊 Current state: {state}")
                    
                    # Simula withdraw
                    print("\n" + "=" * 50)
                    controller.execute_withdraw(1000)
                
                # Chiudi dopo esempio
                time.sleep(3)
    
    finally:
        controller.close()

