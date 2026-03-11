#!/usr/bin/env python3
"""
🔍 Site Analyzer - Analisi DOM del sito per identificare elementi
================================================================

Analizza il codice HTML/CSS/JavaScript del sito per capire come sono
strutturati gli elementi del gioco e genera selettori specifici.
"""
import time
import json
import re
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict

try:
    from playwright.sync_api import Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

@dataclass
class SiteElementProfile:
    """Profilo di un elemento trovato nel sito"""
    element_type: str  # 'chip', 'action', 'card', 'betting_area', ecc.
    selector: str
    text_content: Optional[str] = None
    attributes: Dict[str, str] = None
    classes: List[str] = None
    id: Optional[str] = None
    confidence: float = 0.0  # 0.0-1.0, quanto siamo sicuri che sia corretto
    examples: List[Dict] = None  # Esempi trovati nella pagina

class SiteAnalyzer:
    """Analizza il DOM del sito per identificare elementi del gioco"""
    
    def __init__(self, page: Page):
        self.page = page
        self.profiles: Dict[str, List[SiteElementProfile]] = {}
        self.analyzed = False
    
    def analyze_site(self) -> Dict[str, Any]:
        """Analizza completamente il sito e genera profili degli elementi"""
        print("🔍 Inizio analisi DOM del sito...")
        
        # Attendi che la pagina sia completamente caricata
        self.page.wait_for_load_state("networkidle", timeout=10000)
        time.sleep(2)  # Attesa extra per JavaScript dinamico
        
        analysis = {
            'chips': self._analyze_chips(),
            'actions': self._analyze_actions(),
            'cards': self._analyze_cards(),
            'betting_areas': self._analyze_betting_areas(),
            'balance': self._analyze_balance(),
            'game_state': self._analyze_game_state(),
            'metadata': {
                'url': self.page.url,
                'title': self.page.title(),
                'timestamp': time.time()
            }
        }
        
        self.profiles = analysis
        self.analyzed = True
        
        print("✅ Analisi completata!")
        return analysis
    
    def _analyze_chips(self) -> List[SiteElementProfile]:
        """Analizza e identifica tutti i chip disponibili"""
        print("   🎲 Analizzando chips...")
        profiles = []
        
        try:
            # Esegui JavaScript per trovare tutti i possibili chip
            chips_data = self.page.evaluate("""
                () => {
                    const chips = [];
                    const allElements = document.querySelectorAll('*');
                    
                    allElements.forEach((el, idx) => {
                        // Cerca elementi che potrebbero essere chip
                        const text = el.textContent?.trim() || '';
                        const classList = Array.from(el.classList || []);
                        const id = el.id || '';
                        const tag = el.tagName.toLowerCase();
                        
                        // Pattern per valori chip comuni
                        const chipValues = ['10', '25', '50', '100', '500', '$10', '$25', '$50', '$100', '$500', 
                                          '€10', '€25', '€50', '€100', '€500', '10$', '25$', '50$', '100$', '500$'];
                        
                        // Verifica se sembra un chip
                        const isChip = 
                            classList.some(c => c.toLowerCase().includes('chip') || c.toLowerCase().includes('bet')) ||
                            id.toLowerCase().includes('chip') || id.toLowerCase().includes('bet') ||
                            chipValues.some(v => text.includes(v) || id.includes(v) || classList.some(c => c.includes(v))) ||
                            el.getAttribute('data-value') || el.getAttribute('data-chip') || el.getAttribute('data-bet') ||
                            el.getAttribute('data-amount') || el.getAttribute('aria-label')?.toLowerCase().includes('chip');
                        
                        if (isChip && el.offsetParent !== null) {  // Solo elementi visibili
                            const rect = el.getBoundingClientRect();
                            if (rect.width > 0 && rect.height > 0) {
                                chips.push({
                                    index: idx,
                                    tag: tag,
                                    text: text,
                                    id: id,
                                    classes: classList,
                                    attributes: {
                                        'data-value': el.getAttribute('data-value') || '',
                                        'data-chip': el.getAttribute('data-chip') || '',
                                        'data-bet': el.getAttribute('data-bet') || '',
                                        'data-amount': el.getAttribute('data-amount') || '',
                                        'aria-label': el.getAttribute('aria-label') || '',
                                        'title': el.getAttribute('title') || '',
                                        'onclick': el.getAttribute('onclick') || ''
                                    },
                                    selector: id ? `#${id}` : (classList.length > 0 ? `.${classList[0]}` : tag),
                                    position: {x: rect.x, y: rect.y, width: rect.width, height: rect.height}
                                });
                            }
                        }
                    });
                    
                    return chips;
                }
            """)
            
            # Raggruppa per valore e crea profili
            chip_groups = {}
            for chip in chips_data:
                # Estrai valore del chip
                value = self._extract_chip_value(chip)
                if value:
                    if value not in chip_groups:
                        chip_groups[value] = []
                    chip_groups[value].append(chip)
            
            # Crea profili per ogni valore
            for value, examples in chip_groups.items():
                # Trova il selettore più comune
                best_selector = self._find_best_selector(examples)
                
                profile = SiteElementProfile(
                    element_type='chip',
                    selector=best_selector,
                    text_content=examples[0].get('text', ''),
                    attributes=examples[0].get('attributes', {}),
                    classes=examples[0].get('classes', []),
                    id=examples[0].get('id', ''),
                    confidence=self._calculate_confidence(examples, 'chip'),
                    examples=examples[:5]  # Primi 5 esempi
                )
                profiles.append(profile)
                print(f"      ✅ Chip ${value} trovato: {best_selector} (confidence: {profile.confidence:.2f})")
            
        except Exception as e:
            print(f"      ⚠️ Errore analisi chips: {e}")
        
        return profiles
    
    def _analyze_actions(self) -> List[SiteElementProfile]:
        """Analizza e identifica i pulsanti di azione (Hit, Stand, ecc.)"""
        print("   🎮 Analizzando azioni...")
        profiles = []
        
        action_keywords = {
            'hit': ['hit', 'carta', 'card', 'draw'],
            'stand': ['stand', 'stai', 'stay', 'stop', 'hold'],
            'double': ['double', 'raddoppia', 'doble', 'dbl'],
            'split': ['split', 'dividi', 'divide', 'sep']
        }
        
        try:
            for action, keywords in action_keywords.items():
                action_elements = self.page.evaluate(f"""
                    () => {{
                        const elements = [];
                        const allElements = document.querySelectorAll('button, a, [role="button"], [onclick]');
                        
                        allElements.forEach((el) => {{
                            const text = (el.textContent || '').toLowerCase();
                            const ariaLabel = (el.getAttribute('aria-label') || '').toLowerCase();
                            const title = (el.getAttribute('title') || '').toLowerCase();
                            const classList = Array.from(el.classList || []);
                            const id = el.id || '';
                            const dataAction = (el.getAttribute('data-action') || '').toLowerCase();
                            
                            const keywords = {keywords};
                            const matches = keywords.some(kw => 
                                text.includes(kw) || 
                                ariaLabel.includes(kw) || 
                                title.includes(kw) ||
                                classList.some(c => c.toLowerCase().includes(kw)) ||
                                id.toLowerCase().includes(kw) ||
                                dataAction.includes(kw)
                            );
                            
                            if (matches && el.offsetParent !== null) {  // Visibile
                                const rect = el.getBoundingClientRect();
                                if (rect.width > 0 && rect.height > 0) {{
                                    elements.push({{
                                        tag: el.tagName.toLowerCase(),
                                        text: el.textContent?.trim() || '',
                                        id: id,
                                        classes: classList,
                                        attributes: {{
                                            'data-action': el.getAttribute('data-action') || '',
                                            'aria-label': el.getAttribute('aria-label') || '',
                                            'title': el.getAttribute('title') || '',
                                            'onclick': el.getAttribute('onclick') || ''
                                        }},
                                        selector: id ? `#${{id}}` : (classList.length > 0 ? `.${{classList[0]}}` : el.tagName.toLowerCase()),
                                        position: {{x: rect.x, y: rect.y, width: rect.width, height: rect.height}}
                                    }});
                                }}
                            }}
                        }});
                        
                        return elements;
                    }}
                """)
                
                if action_elements:
                    best_selector = self._find_best_selector(action_elements)
                    profile = SiteElementProfile(
                        element_type=f'action_{action}',
                        selector=best_selector,
                        text_content=action_elements[0].get('text', ''),
                        attributes=action_elements[0].get('attributes', {}),
                        classes=action_elements[0].get('classes', []),
                        id=action_elements[0].get('id', ''),
                        confidence=self._calculate_confidence(action_elements, 'action'),
                        examples=action_elements[:3]
                    )
                    profiles.append(profile)
                    print(f"      ✅ Azione '{action}' trovata: {best_selector} (confidence: {profile.confidence:.2f})")
        
        except Exception as e:
            print(f"      ⚠️ Errore analisi azioni: {e}")
        
        return profiles
    
    def _analyze_cards(self) -> List[SiteElementProfile]:
        """Analizza come sono visualizzate le carte"""
        print("   🎴 Analizzando carte...")
        profiles = []
        
        try:
            cards_data = self.page.evaluate("""
                () => {
                    const cards = [];
                    const allElements = document.querySelectorAll('*');
                    
                    allElements.forEach((el) => {
                        const classList = Array.from(el.classList || []);
                        const id = el.id || '';
                        const text = el.textContent?.trim() || '';
                        
                        // Pattern per carte
                        const isCard = 
                            classList.some(c => c.toLowerCase().includes('card')) ||
                            id.toLowerCase().includes('card') ||
                            /[AKQJ]|[2-9]|10/.test(text) ||
                            el.getAttribute('data-card') ||
                            el.getAttribute('data-suit');
                        
                        if (isCard && el.offsetParent !== null) {
                            const rect = el.getBoundingClientRect();
                            if (rect.width > 0 && rect.height > 0) {
                                cards.push({
                                    tag: el.tagName.toLowerCase(),
                                    text: text,
                                    id: id,
                                    classes: classList,
                                    attributes: {
                                        'data-card': el.getAttribute('data-card') || '',
                                        'data-suit': el.getAttribute('data-suit') || '',
                                        'data-value': el.getAttribute('data-value') || ''
                                    },
                                    selector: id ? `#${id}` : (classList.length > 0 ? `.${classList[0]}` : el.tagName.toLowerCase()),
                                    position: {x: rect.x, y: rect.y, width: rect.width, height: rect.height}
                                });
                            }
                        }
                    });
                    
                    return cards;
                }
            """)
            
            if cards_data:
                best_selector = self._find_best_selector(cards_data)
                profile = SiteElementProfile(
                    element_type='card',
                    selector=best_selector,
                    text_content=cards_data[0].get('text', ''),
                    attributes=cards_data[0].get('attributes', {}),
                    classes=cards_data[0].get('classes', []),
                    id=cards_data[0].get('id', ''),
                    confidence=self._calculate_confidence(cards_data, 'card'),
                    examples=cards_data[:5]
                )
                profiles.append(profile)
                print(f"      ✅ Carte trovate: {best_selector} (confidence: {profile.confidence:.2f})")
        
        except Exception as e:
            print(f"      ⚠️ Errore analisi carte: {e}")
        
        return profiles
    
    def _analyze_betting_areas(self) -> List[SiteElementProfile]:
        """Analizza le aree di betting"""
        print("   🎯 Analizzando aree betting...")
        profiles = []
        
        try:
            # Cerca canvas
            canvas_count = self.page.locator("canvas").count()
            if canvas_count > 0:
                for i in range(canvas_count):
                    canvas = self.page.locator("canvas").nth(i)
                    box = canvas.bounding_box()
                    if box:
                        profile = SiteElementProfile(
                            element_type='betting_area_canvas',
                            selector='canvas',
                            confidence=0.8,
                            examples=[{'index': i, 'size': {'width': box['width'], 'height': box['height']}}]
                        )
                        profiles.append(profile)
                        print(f"      ✅ Canvas betting trovato (index: {i})")
            
            # Cerca div/aree con classi comuni
            areas_data = self.page.evaluate("""
                () => {
                    const areas = [];
                    const selectors = ['.betting-area', '.bet-area', '.bet-zone', '.table-bet', 
                                     '.game-table', '.blackjack-table', '.table', '[data-bet-area]'];
                    
                    selectors.forEach(sel => {
                        try {
                            const elements = document.querySelectorAll(sel);
                            elements.forEach((el, idx) => {
                                if (el.offsetParent !== null) {
                                    const rect = el.getBoundingClientRect();
                                    if (rect.width > 50 && rect.height > 50) {  // Minimo 50x50
                                        areas.push({
                                            selector: sel,
                                            index: idx,
                                            classes: Array.from(el.classList || []),
                                            id: el.id || '',
                                            size: {width: rect.width, height: rect.height},
                                            position: {x: rect.x, y: rect.y}
                                        });
                                    }
                                }
                            });
                        } catch(e) {}
                    });
                    
                    return areas;
                }
            """)
            
            for area in areas_data:
                profile = SiteElementProfile(
                    element_type='betting_area',
                    selector=area['selector'],
                    id=area.get('id', ''),
                    classes=area.get('classes', []),
                    confidence=0.7,
                    examples=[area]
                )
                profiles.append(profile)
                print(f"      ✅ Area betting trovata: {area['selector']}")
        
        except Exception as e:
            print(f"      ⚠️ Errore analisi aree betting: {e}")
        
        return profiles
    
    def _analyze_balance(self) -> List[SiteElementProfile]:
        """Analizza come è visualizzato il balance"""
        print("   💰 Analizzando balance...")
        profiles = []
        
        try:
            balance_elements = self.page.evaluate("""
                () => {
                    const elements = [];
                    const allElements = document.querySelectorAll('*');
                    
                    allElements.forEach((el) => {
                        const text = el.textContent?.trim() || '';
                        const classList = Array.from(el.classList || []);
                        const id = el.id || '';
                        
                        // Pattern per balance (contiene $, €, numeri)
                        const isBalance = 
                            classList.some(c => c.toLowerCase().includes('balance') || c.toLowerCase().includes('money') || c.toLowerCase().includes('credit')) ||
                            id.toLowerCase().includes('balance') || id.toLowerCase().includes('money') || id.toLowerCase().includes('credit') ||
                            (/[\\$€]?\\d+[.,]?\\d*/.test(text) && (text.length < 20));  // Numero con simbolo, testo corto
                        
                        if (isBalance && el.offsetParent !== null) {
                            const rect = el.getBoundingClientRect();
                            if (rect.width > 0 && rect.height > 0) {
                                elements.push({
                                    tag: el.tagName.toLowerCase(),
                                    text: text,
                                    id: id,
                                    classes: classList,
                                    selector: id ? `#${id}` : (classList.length > 0 ? `.${classList[0]}` : el.tagName.toLowerCase())
                                });
                            }
                        }
                    });
                    
                    return elements;
                }
            """)
            
            if balance_elements:
                best_selector = self._find_best_selector(balance_elements)
                profile = SiteElementProfile(
                    element_type='balance',
                    selector=best_selector,
                    text_content=balance_elements[0].get('text', ''),
                    id=balance_elements[0].get('id', ''),
                    classes=balance_elements[0].get('classes', []),
                    confidence=self._calculate_confidence(balance_elements, 'balance'),
                    examples=balance_elements[:3]
                )
                profiles.append(profile)
                print(f"      ✅ Balance trovato: {best_selector} (confidence: {profile.confidence:.2f})")
        
        except Exception as e:
            print(f"      ⚠️ Errore analisi balance: {e}")
        
        return profiles
    
    def _analyze_game_state(self) -> List[SiteElementProfile]:
        """Analizza indicatori di stato del gioco"""
        print("   📊 Analizzando stato gioco...")
        profiles = []
        
        # Cerca indicatori comuni di stato
        state_indicators = [
            '.game-state', '.round-status', '.hand-status',
            '[data-game-state]', '[data-round]', '[data-hand]'
        ]
        
        for indicator in state_indicators:
            try:
                count = self.page.locator(indicator).count()
                if count > 0:
                    profile = SiteElementProfile(
                        element_type='game_state',
                        selector=indicator,
                        confidence=0.6
                    )
                    profiles.append(profile)
                    print(f"      ✅ Indicatore stato trovato: {indicator}")
            except:
                continue
        
        return profiles
    
    def _extract_chip_value(self, chip_data: Dict) -> Optional[str]:
        """Estrae il valore numerico di un chip"""
        # Prova attributi
        for attr in ['data-value', 'data-chip', 'data-bet', 'data-amount']:
            value = chip_data.get('attributes', {}).get(attr, '')
            if value:
                return str(value)
        
        # Prova testo
        text = chip_data.get('text', '')
        numbers = re.findall(r'\d+', text)
        if numbers:
            return numbers[0]
        
        # Prova ID o classi
        id_text = chip_data.get('id', '')
        classes = chip_data.get('classes', [])
        
        for num in ['10', '25', '50', '100', '500']:
            if num in id_text or any(num in c for c in classes):
                return num
        
        return None
    
    def _find_best_selector(self, examples: List[Dict]) -> str:
        """Trova il selettore migliore basato sugli esempi"""
        if not examples:
            return ""
        
        # Preferisci ID se presente e unico
        ids = [ex.get('id', '') for ex in examples if ex.get('id')]
        if ids and len(set(ids)) == 1:
            return f"#{ids[0]}"
        
        # Preferisci classe comune
        all_classes = []
        for ex in examples:
            classes = ex.get('classes', [])
            all_classes.extend(classes)
        
        # Trova classe più comune
        from collections import Counter
        class_counts = Counter(all_classes)
        if class_counts:
            most_common = class_counts.most_common(1)[0]
            if most_common[1] >= len(examples) * 0.5:  # Presente in almeno 50% degli esempi
                return f".{most_common[0]}"
        
        # Fallback: usa il primo selettore trovato
        return examples[0].get('selector', examples[0].get('tag', 'div'))
    
    def _calculate_confidence(self, examples: List[Dict], element_type: str) -> float:
        """Calcola la confidence che gli esempi siano corretti"""
        if not examples:
            return 0.0
        
        confidence = 0.5  # Base
        
        # Più esempi = più confidence
        if len(examples) >= 3:
            confidence += 0.2
        elif len(examples) >= 2:
            confidence += 0.1
        
        # Se hanno ID unico = più confidence
        ids = [ex.get('id', '') for ex in examples if ex.get('id')]
        if ids and len(set(ids)) == 1:
            confidence += 0.2
        
        # Se hanno classi comuni = più confidence
        all_classes = []
        for ex in examples:
            all_classes.extend(ex.get('classes', []))
        if all_classes:
            from collections import Counter
            class_counts = Counter(all_classes)
            if class_counts.most_common(1)[0][1] >= len(examples):
                confidence += 0.1
        
        return min(1.0, confidence)
    
    def generate_site_config(self) -> Dict[str, Any]:
        """Genera configurazione del sito basata sull'analisi"""
        if not self.analyzed:
            self.analyze_site()
        
        config = {
            'url': self.page.url,
            'selectors': {}
        }
        
        # Estrai selettori per chips
        for profile in self.profiles.get('chips', []):
            value = self._extract_chip_value(profile.examples[0] if profile.examples else {})
            if value:
                config['selectors'][f'chip_{value}'] = profile.selector
        
        # Estrai selettori per azioni
        for profile in self.profiles.get('actions', []):
            action = profile.element_type.replace('action_', '')
            config['selectors'][f'{action}_button'] = profile.selector
        
        # Estrai selettori per altre cose
        if self.profiles.get('betting_areas'):
            config['selectors']['betting_area'] = self.profiles['betting_areas'][0].selector
        
        if self.profiles.get('balance'):
            config['selectors']['balance'] = self.profiles['balance'][0].selector
        
        return config
    
    def save_analysis(self, filepath: str):
        """Salva l'analisi in un file JSON"""
        if not self.analyzed:
            self.analyze_site()
        
        # Converti profili in dict
        data = {}
        for key, profiles in self.profiles.items():
            if key != 'metadata':
                data[key] = [asdict(p) for p in profiles]
            else:
                data[key] = profiles
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Analisi salvata in: {filepath}")
