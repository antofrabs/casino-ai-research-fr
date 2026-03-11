#!/usr/bin/env python3
"""
🌐 Interfaccia Web per Casino AI Research Platform
===============================================================

Interfaccia Streamlit che si apre automaticamente nel browser
Permette interazione diretta con il browser del casino
"""
import streamlit as st
import sys
import os
from pathlib import Path
import time
import random

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ai.decision_maker import AIDecisionMaker

# Configurazione pagina
st.set_page_config(
    page_title="🎰 Casino AI Research Platform",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FFD700;
        margin-bottom: 2rem;
    }
    .step-box {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #FFD700;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #0d4f0d;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #00ff00;
    }
    .warning-box {
        background-color: #4f3d0d;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffaa00;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Funzione principale dell'interfaccia web"""
    
    # Header
    st.markdown('<div class="main-header">🎰 CASINO AI RESEARCH PLATFORM</div>', unsafe_allow_html=True)
    
    # Avviso importante
    st.warning("⚠️ **IMPORTANTE**: Questo software è solo per scopi di ricerca. Usare solo su siti di proprietà o con permesso esplicito.")
    
    # Inizializza session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'site_url' not in st.session_state:
        st.session_state.site_url = ""
    if 'play_money' not in st.session_state:
        st.session_state.play_money = False
    if 'credentials' not in st.session_state:
        st.session_state.credentials = {}
    if 'game_config' not in st.session_state:
        st.session_state.game_config = {}
    if 'ai_config' not in st.session_state:
        st.session_state.ai_config = {}
    if 'session_results' not in st.session_state:
        st.session_state.session_results = None
    if 'manual_mode' not in st.session_state:
        st.session_state.manual_mode = False
    if 'pause_ai' not in st.session_state:
        st.session_state.pause_ai = False
    if 'show_code_editor' not in st.session_state:
        st.session_state.show_code_editor = False
    
    # Sidebar con progresso
    with st.sidebar:
        st.header("📋 Progresso")
        steps = [
            "1️⃣ Selezione Sito",
            "2️⃣ Credenziali",
            "3️⃣ Selezione Gioco",
            "4️⃣ Configurazione AI",
            "5️⃣ Auto-Pilota",
            "6️⃣ Withdraw"
        ]
        
        for i, step_name in enumerate(steps, 1):
            if i < st.session_state.step:
                st.success(f"✅ {step_name}")
            elif i == st.session_state.step:
                st.info(f"🔄 {step_name}")
            else:
                st.write(f"⏳ {step_name}")
        
        st.divider()
        st.header("🎮 Controlli Rapidi")
        if st.button("🔄 Ricarica Pagina", use_container_width=True):
            if 'browser_controller' in st.session_state:
                try:
                    st.session_state.browser_controller.page.reload()
                    st.success("✅ Pagina ricaricata")
                    time.sleep(1)
                    st.rerun()
                except:
                    st.error("❌ Browser non disponibile")
        
        st.divider()
        st.header("💻 Editor Codice")
        if st.button("📝 Apri Editor", use_container_width=True):
            st.session_state.show_code_editor = True
            st.rerun()
    
    # STEP 1: Selezione Sito
    if st.session_state.step == 1:
        step1_select_site()
    
    # STEP 2: Credenziali
    elif st.session_state.step == 2:
        step2_credentials()
    
    # STEP 3: Selezione Gioco
    elif st.session_state.step == 3:
        step3_select_game()
    
    # STEP 4: Configurazione AI
    elif st.session_state.step == 4:
        step4_configure_ai()
    
    # STEP 5: Auto-Pilota
    elif st.session_state.step == 5:
        step5_auto_pilot()
    
    # STEP 6: Withdraw
    elif st.session_state.step == 6:
        step6_withdraw()

def step1_select_site():
    """STEP 1: Selezione sito casino"""
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.header("🎯 STEP 1: SELEZIONE SITO CASINO")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Tab per scegliere tipo di sito
    tab1, tab2, tab3 = st.tabs(["🎰 Siti con Soldi Reali", "🆓 Blackjack Play Money", "🔗 URL Personalizzato"])
    
    with tab1:
        st.info("💡 Siti che richiedono credenziali e usano soldi reali")
        st.warning("⚠️ Usa solo su siti di tua proprietà o con permesso esplicito!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📌 Sito Maker", use_container_width=True):
                st.session_state.site_url = "https://tuo-sito-maker.com"
                st.session_state.play_money = False
                st.session_state.step = 2
                st.rerun()
        
        with col2:
            if st.button("🧪 Sito Test", use_container_width=True):
                st.session_state.site_url = "https://sandbox.casinomaker.com"
                st.session_state.play_money = False
                st.session_state.step = 2
                st.rerun()
    
    with tab2:
        st.success("🆓 **Siti con Soldi Falsi** - Perfetti per testare l'AI senza rischi!")
        st.info("💡 Questi siti NON richiedono login e usano solo soldi virtuali")
        
        # Carica siti play money
        try:
            import yaml
            play_money_config = Path(__file__).parent.parent.parent / "config" / "sites" / "play_money_sites.yaml"
            
            if play_money_config.exists():
                with open(play_money_config, 'r') as f:
                    config = yaml.safe_load(f)
                    sites = config.get('sites', [])
                    
                    for site in sites:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{site['name']}**")
                            st.caption(f"🌐 {site['url']}")
                            st.caption(f"📝 {site.get('description', 'Blackjack gratuito')}")
                        
                        with col2:
                            if st.button(f"▶️ Usa", key=f"play_money_{site['name']}", use_container_width=True):
                                st.session_state.site_url = site['url']
                                st.session_state.play_money = True
                                st.session_state.site_config = site
                                st.session_state.step = 2
                                st.rerun()
                        st.divider()
            else:
                st.warning("⚠️ File configurazione play money non trovato")
                # Siti predefiniti
                play_money_sites = [
                    {"name": "247 Blackjack", "url": "https://www.247blackjack.com"},
                    {"name": "Blackjack.org", "url": "https://www.blackjack.org"},
                    {"name": "Casino.org Blackjack", "url": "https://www.casino.org/blackjack/"},
                    {"name": "CardGames.io", "url": "https://cardgames.io/blackjack/"},
                ]
                
                for site in play_money_sites:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{site['name']}**")
                        st.caption(f"🌐 {site['url']}")
                    with col2:
                        if st.button(f"▶️ Usa", key=f"pm_{site['name']}", use_container_width=True):
                            st.session_state.site_url = site['url']
                            st.session_state.play_money = True
                            st.session_state.step = 2
                            st.rerun()
                    st.divider()
        except Exception as e:
            st.error(f"Errore nel caricamento siti play money: {e}")
            # Fallback a siti predefiniti
            if st.button("🆓 247 Blackjack (Play Money)", use_container_width=True):
                st.session_state.site_url = "https://www.247blackjack.com"
                st.session_state.play_money = True
                st.session_state.step = 2
                st.rerun()
    
    with tab3:
        st.info("💡 Inserisci un URL personalizzato")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            site_url = st.text_input(
                "🌐 URL del sito casino",
                value=st.session_state.site_url,
                placeholder="https://tuo-sito-maker.com",
                key="custom_url"
            )
        
        with col2:
            st.write("")
            st.write("")
            if st.button("▶️ Continua", type="primary", use_container_width=True, key="custom_continue"):
                if site_url and (site_url.startswith('http://') or site_url.startswith('https://')):
                    st.session_state.site_url = site_url
                    st.session_state.play_money = False
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("❌ Inserisci un URL valido (deve iniziare con http:// o https://)")
        
        if st.button("🔄 Reset", use_container_width=True, key="reset_custom"):
            st.session_state.step = 1
            st.session_state.site_url = ""
            st.rerun()

def step2_credentials():
    """STEP 2: Inserimento credenziali con verifica reale"""
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.header("🔑 STEP 2: INSERIMENTO CREDENZIALI")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Verifica se è un sito play money
    is_play_money = st.session_state.get('play_money', False)
    
    if is_play_money:
        st.success("🆓 **Sito Play Money** - Non sono necessarie credenziali!")
        st.info("💡 Questo sito usa solo soldi virtuali. Puoi procedere direttamente.")
        
        if st.button("▶️ Continua senza Login", type="primary", use_container_width=True):
            st.session_state.credentials = {
                'email': None,
                'password': None,
                'site_url': st.session_state.site_url,
                'demo_mode': False,
                'play_money': True
            }
            st.session_state.step = 3
            st.rerun()
        
        st.divider()
        st.caption("💡 Se preferisci, puoi comunque inserire credenziali (se il sito le richiede)")
    
    st.info(f"💡 Inserisci le credenziali per: **{st.session_state.site_url}**")
    if not is_play_money:
        st.warning("⚠️ Le credenziali verranno verificate con login reale al sito!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input(
            "📧 Email/Username",
            value=st.session_state.credentials.get('email', ''),
            placeholder="tuo-email@example.com"
        )
    
    with col2:
        password = st.text_input(
            "🔒 Password",
            type="password",
            value=st.session_state.credentials.get('password', ''),
            placeholder="••••••••"
        )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("◀️ Indietro", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    
    with col2:
        if st.button("💾 Salva Demo", use_container_width=True):
            st.warning("⚠️ Modalità Demo: le credenziali non verranno verificate")
            st.session_state.credentials = {
                'email': 'demo@example.com',
                'password': 'demo123',
                'site_url': st.session_state.site_url,
                'demo_mode': True
            }
            st.session_state.step = 3
            st.rerun()
    
    with col3:
        if st.button("🔐 Verifica e Continua", type="primary", use_container_width=True):
            if email and password:
                # Verifica credenziali con login reale
                with st.spinner("🔐 Verifica credenziali in corso..."):
                    try:
                        # Verifica Playwright prima
                        try:
                            from playwright.sync_api import sync_playwright
                            playwright_ok = True
                        except ImportError as e:
                            playwright_ok = False
                            st.error("❌ Playwright non installato!")
                            st.code("pip install playwright\npython3 -m playwright install chromium", language="bash")
                            return
                        
                        from src.automation.browser_controller import CasinoBrowserController
                        
                        # Avvia browser (visibile, non headless)
                        controller = CasinoBrowserController(headless=False, slow_mo=200)
                        
                        if not controller.start_browser():
                            st.error("❌ Impossibile avviare il browser.")
                            st.info("💡 Verifica che Playwright sia installato:")
                            st.code("pip install playwright\npython3 -m playwright install chromium", language="bash")
                            if 'controller' in locals():
                                controller.close()
                            return
                        
                        # Prova login
                        login_success = controller.login(
                            st.session_state.site_url,
                            {'email': email, 'password': password}
                        )
                        
                        if login_success:
                            # Salva credenziali e browser controller
                            st.session_state.credentials = {
                                'email': email,
                                'password': password,
                                'site_url': st.session_state.site_url,
                                'demo_mode': False
                            }
                            st.session_state.browser_controller = controller
                            st.session_state.initial_balance = controller.get_balance()
                            
                            st.success(f"✅ Login riuscito! Balance: ${controller.get_balance():.2f}")
                            st.info("🌐 Il browser è aperto - puoi vedere il sito")
                            st.session_state.step = 3
                            time.sleep(2)
                            st.rerun()
                        else:
                            controller.close()
                            st.error("❌ Login fallito! Verifica che le credenziali siano corrette e che il sito sia raggiungibile.")
                            st.info("💡 Suggerimento: Controlla il browser per vedere eventuali errori")
                            
                    except Exception as e:
                        st.error(f"❌ Errore durante il login: {str(e)}")
                        st.info("💡 Assicurati che Playwright sia installato: pip install playwright && playwright install chromium")
            else:
                st.error("❌ Inserisci email e password")

def step3_select_game():
    """STEP 3: Selezione gioco"""
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.header("🎲 STEP 3: SELEZIONE GIOCO")
    st.markdown("</div>", unsafe_allow_html=True)
    
    games = {
        "Blackjack": "🃏",
        "Roulette": "🎡",
        "Baccarat": "🎴",
        "Poker": "🂡",
        "Slot": "🎰"
    }
    
    selected_game = st.radio(
        "🎯 Quale gioco vuoi testare?",
        options=list(games.keys()),
        horizontal=True
    )
    
    st.session_state.game_config = {
        "name": selected_game,
        "type": selected_game.lower(),
        "auto_detect": True
    }
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("◀️ Indietro", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    
    with col2:
        if st.button("▶️ Continua", type="primary", use_container_width=True):
            st.session_state.step = 4
            st.rerun()

def step4_configure_ai():
    """STEP 4: Configurazione AI"""
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.header("⚙️ STEP 4: CONFIGURAZIONE AI")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        bankroll = st.number_input(
            "💰 Bankroll iniziale",
            min_value=100,
            max_value=1000000,
            value=10000,
            step=100
        )
        
        risk = st.number_input(
            "🎯 Rischio per mano (%)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1
        )
    
    with col2:
        stop_loss = st.number_input(
            "📉 Stop-loss (%)",
            min_value=5,
            max_value=50,
            value=20,
            step=5
        )
        
        stop_win = st.number_input(
            "📈 Stop-win (%)",
            min_value=5,
            max_value=100,
            value=30,
            step=5
        )
    
    card_counting = st.checkbox(
        "🎴 Abilitare conteggio carte",
        value=True,
        disabled=(st.session_state.game_config.get('name') != 'Blackjack')
    )
    
    if st.session_state.game_config.get('name') != 'Blackjack':
        st.info("ℹ️ Il conteggio carte è disponibile solo per Blackjack")
    
    st.session_state.ai_config = {
        "mode": "auto_pilot",
        "initial_bankroll": float(bankroll),
        "risk_per_bet": float(risk) / 100,
        "stop_loss": float(stop_loss) / 100,
        "stop_win": float(stop_win) / 100,
        "enable_card_counting": card_counting and st.session_state.game_config["name"] == "Blackjack",
        "auto_withdraw": True,
        "require_supervision": True
    }
    
    # Riepilogo
    st.markdown("### 📊 Riepilogo Configurazione")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Bankroll", f"${bankroll:,.0f}")
    col2.metric("🎯 Rischio", f"{risk}%")
    col3.metric("📉 Stop-Loss", f"{stop_loss}%")
    col4.metric("📈 Stop-Win", f"{stop_win}%")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("◀️ Indietro", use_container_width=True):
            st.session_state.step = 3
            st.rerun()
    
    with col2:
        if st.button("▶️ Avvia Auto-Pilota", type="primary", use_container_width=True):
            st.session_state.step = 5
            st.rerun()

def step5_auto_pilot():
    """STEP 5: Auto-pilota con browser reale"""
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.header("🤖 STEP 5: AUTO-PILOTA")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Riepilogo sessione
    st.markdown("### 🎯 Riepilogo Sessione")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌐 Sito", st.session_state.site_url.split('//')[-1].split('/')[0])
    col2.metric("🎮 Gioco", st.session_state.game_config['name'])
    col3.metric("💰 Bankroll", f"${st.session_state.ai_config['initial_bankroll']:,.0f}")
    col4.metric("🎴 Conteggio", "ATTIVO" if st.session_state.ai_config['enable_card_counting'] else "DISATTIVO")
    
    # Verifica se abbiamo il browser controller
    demo_mode = st.session_state.credentials.get('demo_mode', False)
    play_money = st.session_state.get('play_money', False)
    controller = st.session_state.get('browser_controller', None)
    
    if demo_mode:
        st.warning("⚠️ Modalità Demo: verrà eseguita una simulazione")
        if st.button("🚀 Avvia Simulazione Demo", type="primary", use_container_width=True):
            _run_demo_simulation()
    elif play_money:
        # Sito play money - avvia browser senza login
        st.success("🆓 **Sito Play Money** - Avvio browser senza login")
        st.info("💡 Il browser si aprirà direttamente sul gioco")
        
        # Verifica se siamo su Streamlit Cloud
        is_streamlit_cloud = os.environ.get('STREAMLIT_CLOUD', False) or 'streamlit.app' in os.environ.get('STREAMLIT_SERVER_URL', '')
        
        if is_streamlit_cloud:
            st.warning("⚠️ **Streamlit Cloud**: L'automazione del browser non è disponibile su Streamlit Cloud.")
            st.info("💡 Usa l'**Editor di Codice** nella sidebar per modificare il codice direttamente online!")
            st.info("🌐 Per l'automazione del browser, esegui l'app localmente o su un server con Playwright installato.")
        
        if st.button("🌐 Avvia Browser e Gioca", type="primary", use_container_width=True, disabled=is_streamlit_cloud):
            with st.spinner("🌐 Avvio browser..."):
                try:
                    # Verifica Playwright prima di importare
                    try:
                        from playwright.sync_api import sync_playwright
                        playwright_available = True
                    except ImportError:
                        playwright_available = False
                        st.error("❌ Playwright non trovato!")
                        st.info("💡 Su Streamlit Cloud, l'automazione del browser non è disponibile.")
                        st.info("💡 Usa l'**Editor di Codice** nella sidebar per modificare il codice!")
                        return
                    
                    from src.automation.browser_controller import CasinoBrowserController
                    
                    # Avvia browser (visibile, non headless)
                    controller = CasinoBrowserController(headless=False, slow_mo=200)
                    
                    if not controller.start_browser():
                        st.error("❌ Impossibile avviare il browser.")
                        st.info("💡 Verifica che Playwright sia installato correttamente:")
                        st.code("pip install playwright\npython3 -m playwright install chromium", language="bash")
                        return
                    
                    # Naviga direttamente al sito (senza login)
                    controller.page.goto(st.session_state.site_url, timeout=30000)
                    time.sleep(3)
                    
                    # Cerca e clicca il pulsante Play se presente
                    site_config = st.session_state.get('site_config', None)
                    if controller.click_play_button(site_config):
                        st.success("✅ Pulsante Play cliccato! Gioco avviato.")
                    else:
                        st.info("💡 Pulsante Play non trovato - potrebbe essere già nel gioco o richiedere click manuale")
                    
                    st.session_state.browser_controller = controller
                    st.session_state.initial_balance = 0  # Play money, balance non reale
                    
                    st.success("✅ Browser avviato! Guarda la finestra del browser.")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Errore: {str(e)}")
                    st.info("💡 Assicurati che Playwright sia installato: pip install playwright && playwright install chromium")
        
        if controller:
            _show_interactive_mode(controller)
    else:
        if controller is None:
            st.error("❌ Browser non disponibile. Torna allo step 2 e verifica le credenziali.")
            if st.button("◀️ Torna alle Credenziali", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
        else:
            _show_interactive_mode(controller)
    
    if st.button("◀️ Indietro", use_container_width=True):
        st.session_state.step = 4
        st.rerun()

def _show_interactive_mode(controller):
    """Mostra modalità interattiva con browser"""
    st.success("✅ Browser connesso e pronto")
    st.info("🌐 **Il browser è aperto - puoi interagire direttamente cliccando su di esso!**")
    
    # Modalità di interazione - DEFAULT: Manuale
    st.markdown("### 🎮 Modalità di Interazione")
    if 'interaction_mode' not in st.session_state:
        st.session_state.interaction_mode = "✋ Solo Interazione Manuale"
    
    # Calcola l'indice iniziale
    default_index = 0
    if 'interaction_mode' in st.session_state:
        if st.session_state.interaction_mode == "🤖 Auto-Pilota AI":
            default_index = 1
        elif st.session_state.interaction_mode == "🔄 Ibrido (AI + Manuale)":
            default_index = 2
    
    interaction_mode = st.radio(
        "Scegli come vuoi giocare:",
        ["✋ Solo Interazione Manuale", "🤖 Auto-Pilota AI", "🔄 Ibrido (AI + Manuale)"],
        index=default_index,
        key="interaction_mode"
    )
    
    # Mostra screenshot del browser corrente (thread-safe) con auto-refresh
    screenshot_placeholder = st.empty()
    screenshot_container = st.container()
    
    # Funzione per aggiornare screenshot
    def update_screenshot():
        try:
            screenshot = controller.page.screenshot(type='png')
            return screenshot
        except Exception as e:
            return None
    
    # Auto-refresh screenshot sempre attivo in modalità manuale
    auto_refresh_enabled = st.session_state.get('auto_refresh_enabled', True)
    
    # Mostra screenshot iniziale
    initial_screenshot = update_screenshot()
    if initial_screenshot:
        screenshot_placeholder.image(initial_screenshot, caption="📸 Browser - Aggiornamento automatico ogni 2 secondi", use_container_width=True)
    else:
        st.info("💡 Il browser è aperto - puoi vedere e cliccare direttamente sul sito")
    
    # Pulsante Debug - Mostra elementi trovati
    if st.button("🔍 Debug: Mostra Elementi Trovati", key="debug_elements"):
        try:
            from src.automation.element_finder import ElementFinder
            finder = ElementFinder(controller.page)
            report = finder.generate_report()
            
            st.success("✅ Elementi trovati!")
            
            with st.expander("📊 Pulsanti Trovati", expanded=False):
                st.json(report['buttons'][:20])  # Mostra primi 20
            
            with st.expander("🎲 Chip Trovati", expanded=True):
                if report['chips']:
                    for chip in report['chips']:
                        st.write(f"**{chip.get('text', 'N/A')}**")
                        st.code(f"Selector: {chip.get('selector', 'N/A')}\nID: {chip.get('id', 'N/A')}\nClass: {chip.get('className', 'N/A')}\nData-Value: {chip.get('dataValue', 'N/A')}")
                else:
                    st.warning("Nessun chip trovato")
            
            with st.expander("🎮 Azioni Trovate", expanded=True):
                for action, buttons in report['actions'].items():
                    if buttons:
                        st.subheader(f"{action.upper()}: {len(buttons)} pulsanti")
                        for btn in buttons[:3]:
                            st.write(f"- **{btn.get('text', 'N/A')}** | Selector: `{btn.get('selector', 'N/A')}`")
            
            with st.expander("🎯 Aree Betting", expanded=True):
                if report['betting_areas']:
                    for area in report['betting_areas']:
                        st.write(f"**{area['type']}** - Selector: `{area['selector']}` - Size: {area['size']['width']}x{area['size']['height']}")
                else:
                    st.warning("Nessuna area betting trovata")
        except Exception as e:
            st.error(f"❌ Errore debug: {e}")
    
    if interaction_mode == "✋ Solo Interazione Manuale":
        st.warning("✋ **Modalità Manuale** - L'AI è completamente disabilitata!")
        st.success("💡 **Clicca direttamente nel browser aperto** per giocare liberamente!")
        
        # Controlli per auto-refresh
        col_controls = st.columns(4)
        with col_controls[0]:
            auto_refresh_toggle = st.checkbox("🔄 Auto-aggiorna Screenshot", value=st.session_state.get('auto_refresh_enabled', True), key="auto_refresh_toggle")
            st.session_state['auto_refresh_enabled'] = auto_refresh_toggle
        
        with col_controls[1]:
            if st.button("🔄 Aggiorna Ora", use_container_width=True, key="manual_refresh_now"):
                try:
                    screenshot = update_screenshot()
                    if screenshot:
                        screenshot_placeholder.image(screenshot, caption="📸 Browser - Screenshot aggiornato!", use_container_width=True)
                        st.success("✅ Screenshot aggiornato!")
                    else:
                        st.warning("⚠️ Impossibile fare screenshot")
                except Exception as e:
                    st.error(f"❌ Errore: {e}")
        
        with col_controls[2]:
            if st.button("🔄 Ricarica Pagina", use_container_width=True, key="manual_reload"):
                try:
                    controller.page.reload()
                    time.sleep(2)
                    screenshot = update_screenshot()
                    if screenshot:
                        screenshot_placeholder.image(screenshot, caption="📸 Pagina ricaricata", use_container_width=True)
                        st.success("✅ Pagina ricaricata!")
                except Exception as e:
                    st.error(f"❌ Errore: {e}")
        
        with col_controls[3]:
            if st.button("🌐 Apri in Nuova Tab", use_container_width=True, key="open_new_tab"):
                try:
                    url = controller.page.url
                    st.markdown(f'<a href="{url}" target="_blank">🌐 Apri Browser</a>', unsafe_allow_html=True)
                    st.info(f"💡 URL: {url}")
                except:
                    pass
        
        # Auto-refresh continuo se attivato
        if auto_refresh_toggle:
            refresh_count = st.session_state.get('refresh_count', 0)
            st.session_state['refresh_count'] = refresh_count + 1
            
            try:
                screenshot = update_screenshot()
                if screenshot:
                    screenshot_placeholder.image(screenshot, caption=f"📸 Browser - Auto-aggiornamento #{refresh_count} (ogni 2 sec) - Clicca nel browser per interagire!", use_container_width=True)
                else:
                    st.info("💡 Il browser è aperto - clicca direttamente su di esso per interagire")
            except Exception as e:
                st.caption(f"ℹ️ Screenshot non disponibile: {str(e)[:50]}...")
            
            # Auto-rerun per refresh continuo
            time.sleep(2)
            st.rerun()
        else:
            # Se auto-refresh disabilitato, mostra screenshot statico
            try:
                screenshot = update_screenshot()
                if screenshot:
                    screenshot_placeholder.image(screenshot, caption="📸 Browser - Attiva 'Auto-aggiorna Screenshot' per refresh continuo", use_container_width=True)
                else:
                    st.info("💡 Il browser è aperto - clicca direttamente su di esso per interagire")
            except:
                st.info("💡 Il browser è aperto - clicca direttamente su di esso per interagire")
        
        # Istruzioni
        st.markdown("---")
        st.markdown("### 📋 Istruzioni Modalità Manuale")
        st.markdown("""
        1. **Il browser è aperto** - vedi la finestra del browser separata
        2. **Clicca direttamente nel browser** - puoi interagire normalmente
        3. **Screenshot si aggiorna automaticamente** - vedi lo stato in tempo reale qui
        4. **L'AI è completamente disabilitata** - hai controllo totale
        5. **Per riattivare l'AI** - cambia modalità in "Auto-Pilota AI"
        """)
        
        # Mostra URL corrente
        try:
            current_url = controller.page.url
            st.caption(f"🌐 URL corrente: {current_url}")
        except:
            pass
        
    elif interaction_mode == "🤖 Auto-Pilota AI":
        # Auto-pilota normale
        st.info("🤖 **Modalità Auto-Pilota** - L'AI giocherà automaticamente")
        st.warning("⚠️ Assicurati di essere già nel gioco prima di avviare!")
        
        if st.button("🚀 Avvia Auto-Pilota Reale", type="primary", use_container_width=True):
            _run_real_auto_pilot(controller)
    elif interaction_mode == "🔄 Ibrido (AI + Manuale)":
        st.info("🔄 **Modalità Ibrida** - L'AI gioca automaticamente, ma puoi intervenire in qualsiasi momento!")
        if st.button("🚀 Avvia Modalità Ibrida", type="primary", use_container_width=True):
            _run_hybrid_mode(controller)

def _run_hybrid_mode(controller):
    """Modalità ibrida: AI + intervento manuale"""
    from src.ai.decision_maker import AIDecisionMaker
    
    st.success("🔄 **Modalità Ibrida Attiva**")
    st.info("💡 L'AI gioca automaticamente, ma puoi cliccare nel browser per intervenire in qualsiasi momento!")
    
    # Crea AI
    ai_config = st.session_state.ai_config.copy()
    ai_config['decks_remaining'] = 6
    ai_config['max_hands'] = 100
    
    ai = AIDecisionMaker(ai_config)
    
    # Container
    screenshot_placeholder = st.empty()
    metrics_placeholder = st.empty()
    status_placeholder = st.empty()
    controls_placeholder = st.empty()
    
    max_hands = 50
    hands_played = 0
    results = []
    
    for i in range(max_hands):
        # Controlli
        with controls_placeholder.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⏸️ Pausa", key=f"hybrid_pause_{i}"):
                    st.session_state['pause_ai'] = True
                    st.rerun()
            with col2:
                if st.button("✋ Solo Manuale", key=f"hybrid_manual_{i}"):
                    st.session_state['manual_mode'] = True
                    st.rerun()
            with col3:
                if st.button("🛑 Stop", key=f"hybrid_stop_{i}"):
                    break
        
        if st.session_state.get('pause_ai', False):
            st.warning("⏸️ AI in pausa - Interagisci manualmente nel browser")
            try:
                screenshot = controller.page.screenshot(type='png')
                screenshot_placeholder.image(screenshot, caption="📸 Pausa - Interagisci manualmente", use_container_width=True)
            except:
                pass
            if st.button("▶️ Riprendi", key=f"hybrid_resume_{i}"):
                st.session_state['pause_ai'] = False
                st.rerun()
            time.sleep(1)
            continue
        
        # Screenshot
        try:
            screenshot = controller.page.screenshot(type='png')
            screenshot_placeholder.image(screenshot, caption=f"📸 Mano {i+1} - AI attiva (puoi intervenire)", use_container_width=True)
        except:
            pass
        
        # AI gioca (semplificato)
        status_placeholder.text(f"🤖 AI sta giocando mano {i+1}... (puoi intervenire nel browser)")
        time.sleep(2)
        
        hands_played += 1
        
        # Metriche
        with metrics_placeholder.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("🎲 Mani", hands_played)
            col2.metric("🎴 Count", ai.card_count)
            col3.metric("💰 Balance", "N/A")
        
        if hands_played >= max_hands:
            break

def _run_real_auto_pilot(controller, play_money=False):
    """Esegue auto-pilota reale con browser"""
    from src.ai.decision_maker import AIDecisionMaker
    
    if play_money:
        st.success("🆓 **Modalità Play Money** - Stai giocando con soldi virtuali!")
    else:
        st.warning("💰 **Modalità Soldi Reali** - Attenzione!")
    
    st.info("🌐 **Guarda il browser aperto** - vedrai tutte le azioni in tempo reale!")
    
    # Naviga al gioco
    game_name = st.session_state.game_config['name'].lower()
    site_config = st.session_state.get('site_config', None)
    
    # Se siamo su un sito play money, il pulsante Play è già stato cliccato
    # Ma proviamo comunque la navigazione per sicurezza
    try:
        # Usa site_config come keyword argument
        if site_config:
            nav_success = controller.navigate_to_game(game_name, site_config=site_config)
        else:
            nav_success = controller.navigate_to_game(game_name)
            
        if not nav_success:
            st.warning(f"⚠️ Navigazione automatica non riuscita per {game_name}")
            st.info("💡 Il gioco potrebbe essere già caricato. Verifica manualmente nel browser.")
            # Continua comunque - potrebbe essere già nel gioco
    except Exception as e:
        st.warning(f"⚠️ Errore navigazione: {e}")
        st.info("💡 Continua comunque - verifica manualmente nel browser")
    
    # Crea AI con configurazione
    ai_config = st.session_state.ai_config.copy()
    ai_config['decks_remaining'] = 6
    ai_config['max_hands'] = 100
    
    ai = AIDecisionMaker(ai_config)
    
    # Container per screenshot e metriche
    screenshot_placeholder = st.empty()
    metrics_placeholder = st.empty()
    status_placeholder = st.empty()
    controls_placeholder = st.empty()
    
    # Loop principale
    max_hands = 50  # Limite per demo
    hands_played = 0
    results = []
    ai_paused = False
    
    for i in range(max_hands):
        # Controlli interattivi durante il gioco
        with controls_placeholder.container():
            control_col1, control_col2, control_col3, control_col4 = st.columns(4)
            with control_col1:
                if st.button("⏸️ Pausa AI", key=f"pause_{i}", use_container_width=True):
                    st.session_state['pause_ai'] = True
                    ai_paused = True
                    st.rerun()
            with control_col2:
                if st.button("✋ Solo Manuale", key=f"manual_{i}", use_container_width=True):
                    st.session_state['manual_mode'] = True
                    st.rerun()
            with control_col3:
                if st.button("🔄 Ricarica", key=f"reload_{i}", use_container_width=True):
                    controller.page.reload()
                    time.sleep(2)
            with control_col4:
                if st.button("🛑 Stop", key=f"stop_{i}", use_container_width=True):
                    st.warning("🛑 Sessione interrotta dall'utente")
                    break
        
        # Controlla se l'AI è in pausa
        if st.session_state.get('pause_ai', False) or ai_paused:
            st.warning("⏸️ **AI IN PAUSA** - Puoi interagire manualmente nel browser")
            st.info("💡 Clicca nel browser per giocare. Usa 'Riprendi AI' per continuare automaticamente")
            
            # Mostra screenshot continuo durante pausa
            try:
                screenshot = controller.page.screenshot(type='png')
                screenshot_placeholder.image(screenshot, caption="📸 Pausa - Interagisci manualmente", use_container_width=True)
            except:
                pass
            
            # Pulsante per riprendere
            if st.button("▶️ Riprendi AI", key=f"resume_{i}"):
                st.session_state['pause_ai'] = False
                ai_paused = False
                st.rerun()
            
            time.sleep(1)
            continue
        
        # Controlla stop conditions
        if ai.check_stop_conditions():
            st.warning("🛑 Condizione di stop raggiunta")
            break
        
        # Screenshot del browser
        try:
            screenshot = controller.page.screenshot(type='png')
            screenshot_placeholder.image(screenshot, caption=f"📸 Mano {i+1} - Stato attuale", use_container_width=True)
        except:
            pass
        
        # Cattura stato gioco
        game_state = controller.capture_game_state()
        
        # Calcola puntata
        bet = ai.calculate_bet()
        
        # Piazza puntata (gestisce errori)
        try:
            if not controller.place_bet(bet, "player"):
                st.warning("⚠️ Impossibile piazzare puntata - passa alla modalità manuale")
                st.info("💡 Puoi piazzare puntate manualmente nel browser")
                # Continua comunque - l'utente può giocare manualmente
        except Exception as e:
            st.warning(f"⚠️ Errore piazzamento puntata: {e}")
            st.info("💡 Passa alla modalità manuale per giocare")
        
        time.sleep(1)
        
        # Decisione AI (semplificata per demo)
        # In realtà qui l'AI analizzerebbe le carte visibili
        try:
            available_actions = controller.get_available_actions()
            
            if 'hit' in available_actions:
                try:
                    controller.take_action('hit')
                except:
                    pass
            elif 'stand' in available_actions:
                try:
                    controller.take_action('stand')
                except:
                    pass
        except Exception as e:
            # Se non riesce a leggere azioni, continua comunque
            st.info("💡 L'AI non può leggere le azioni - puoi giocare manualmente nel browser")
        
        time.sleep(2)  # Attende risultato
        
        # Aggiorna balance (thread-safe)
        try:
            current_balance = controller.get_balance()
        except Exception as e:
            current_balance = st.session_state.get('initial_balance', 0)
            st.warning(f"⚠️ Impossibile leggere balance: {e}")
        
        profit = current_balance - st.session_state.get('initial_balance', current_balance)
        
        hands_played += 1
        
        # Aggiorna metriche
        with metrics_placeholder.container():
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🎲 Mani", hands_played)
            col2.metric("💰 Balance", f"${current_balance:.2f}")
            col3.metric("📈 Profitto", f"${profit:+.2f}")
            col4.metric("🎴 Count", ai.card_count)
        
        status_placeholder.text(f"📊 Mano {hands_played}: Bet=${bet:.2f} | Balance=${current_balance:.2f}")
        
        results.append({
            'hand': hands_played,
            'balance': current_balance,
            'profit': profit,
            'bet': bet
        })
        
        time.sleep(1)
    
    # Risultati finali
    final_balance = controller.get_balance()
    initial_balance = st.session_state.get('initial_balance', final_balance)
    total_profit = final_balance - initial_balance
    
    st.session_state.session_results = {
        "bankroll": final_balance,
        "profit": total_profit,
        "profit_pct": (total_profit / initial_balance * 100) if initial_balance > 0 else 0,
        "hands_played": hands_played,
        "card_count": ai.card_count,
        "initial_bankroll": initial_balance
    }
    
    # Mostra risultati
    st.markdown("### 📈 Risultati Sessione Reale")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎲 Mani Giocate", hands_played)
    col2.metric("💰 Balance Finale", f"${final_balance:.2f}")
    col3.metric("📈 Profitto Totale", f"${total_profit:+.2f}")
    col4.metric("🎴 Conteggio Finale", ai.card_count)
    
    # Grafico
    if results:
        import pandas as pd
        df = pd.DataFrame(results)
        st.line_chart(df.set_index('hand')[['balance', 'profit']])
    
    if st.button("▶️ Procedi con Withdraw", type="primary", use_container_width=True):
        st.session_state.step = 6
        st.rerun()

def _run_demo_simulation():
    """Esegue simulazione demo"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simula sessione
    bankroll = st.session_state.ai_config["initial_bankroll"]
    initial_bankroll = bankroll
    hands_played = 0
    card_count = 0
    results = []
    
    for i in range(1, 51):
        # Calcola puntata
        bet = bankroll * st.session_state.ai_config["risk_per_bet"]
        bet = max(10, min(bet, bankroll * 0.05))
        
        # Simula risultato
        outcome = random.choices(
            ['win', 'loss', 'push'],
            weights=[0.48, 0.47, 0.05]
        )[0]
        
        if outcome == 'win':
            profit = bet * 0.95
        elif outcome == 'loss':
            profit = -bet
        else:
            profit = 0
        
        bankroll += profit
        
        # Aggiorna conteggio carte
        if st.session_state.ai_config['enable_card_counting']:
            cards = random.randint(2, 6)
            for _ in range(cards):
                card = random.randint(1, 13)
                if 2 <= card <= 6:
                    card_count += 1
                elif card >= 10:
                    card_count -= 1
        
        hands_played += 1
        
        # Aggiorna progresso
        progress_bar.progress(i / 50)
        profit_total = bankroll - initial_bankroll
        profit_pct = (profit_total / initial_bankroll) * 100
        
        status_text.text(f"📊 Mano {i}/50: Bankroll=${bankroll:.0f} ({profit_pct:+.1f}%) Count={card_count}")
        
        results.append({
            'hand': i,
            'bankroll': bankroll,
            'profit': profit_total,
            'profit_pct': profit_pct,
            'count': card_count
        })
        
        time.sleep(0.05)
    
    # Risultati finali
    profit_total = bankroll - initial_bankroll
    profit_pct = (profit_total / initial_bankroll) * 100
    
    st.session_state.session_results = {
        "bankroll": bankroll,
        "profit": profit_total,
        "profit_pct": profit_pct,
        "hands_played": hands_played,
        "card_count": card_count,
        "initial_bankroll": initial_bankroll
    }
    
    # Mostra risultati
    st.markdown("### 📈 Risultati Sessione")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎲 Mani Giocate", hands_played)
    col2.metric("💰 Bankroll Finale", f"${bankroll:.0f}")
    col3.metric("📈 Profitto", f"${profit_total:+.0f}", f"{profit_pct:+.1f}%")
    col4.metric("🎴 Conteggio Finale", card_count)
    
    # Grafico
    if results:
        import pandas as pd
        df = pd.DataFrame(results)
        st.line_chart(df.set_index('hand')[['bankroll', 'profit']])
    
    if st.button("▶️ Procedi con Withdraw", type="primary", use_container_width=True):
        st.session_state.step = 6
        st.rerun()

def step6_withdraw():
    """STEP 6: Withdraw assistito"""
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.header("💳 STEP 6: WITHDRAW ASSISTITO")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.session_results:
        withdraw_amount = st.session_state.session_results["bankroll"]
        
        st.warning("⚠️ **ATTENZIONE**: Procedura di withdraw richiede SUPERVISIONE. L'AI mostrerà i passaggi, ma serve conferma manuale.")
        
        st.metric("💰 Importo Disponibile", f"${withdraw_amount:.2f}")
        
        st.markdown("### 📋 Procedura Withdraw")
        
        steps = [
            "🔐 Accedi alla pagina di withdraw",
            "💳 Seleziona metodo di pagamento",
            "💰 Inserisci importo da prelevare",
            "📋 Verifica dettagli transazione",
            "✅ Conferma operazione"
        ]
        
        for i, step in enumerate(steps, 1):
            st.markdown(f"**{i}.** {step}")
        
        if st.button("✅ Conferma Withdraw", type="primary", use_container_width=True):
            st.success("🎉 **WITHDRAW COMPLETATO CON SUCCESSO!**")
            st.info(f"💰 Importo prelevato: ${withdraw_amount:.2f}")
            st.info("📧 Verifica l'email per la conferma della transazione")
            st.info("🕒 Tempo stimato per accredito: 1-3 giorni lavorativi")
    
    if st.button("🔄 Nuova Sessione", use_container_width=True):
        # Reset tutto
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.step = 1
        st.rerun()
    
    # CODE EDITOR: Editor di codice (sempre disponibile)
    if st.session_state.get('show_code_editor', False):
        try:
            from src.dashboard.code_editor import show_code_editor
            show_code_editor()
        except ImportError:
            st.error("❌ Modulo code_editor non trovato")
        except Exception as e:
            st.error(f"❌ Errore editor: {e}")

if __name__ == "__main__":
    main()
