#!/usr/bin/env python3
"""
🔍 Element Finder - Rilevamento intelligente elementi del gioco
================================================================

Sistema di debug e rilevamento automatico degli elementi del gioco
per aiutare a configurare i selettori corretti.
"""
from typing import Dict, List, Optional, Any
import json

try:
    from playwright.sync_api import Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class ElementFinder:
    """Trova e analizza elementi del gioco nel browser"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def find_all_buttons(self) -> List[Dict[str, Any]]:
        """Trova tutti i pulsanti nella pagina"""
        buttons = []
        try:
            # Esegui JavaScript per trovare tutti i pulsanti
            buttons_data = self.page.evaluate("""
                () => {
                    const buttons = Array.from(document.querySelectorAll('button, a, [role="button"], [onclick]'));
                    return buttons.map((btn, idx) => ({
                        index: idx,
                        tag: btn.tagName.toLowerCase(),
                        text: btn.textContent?.trim() || '',
                        id: btn.id || '',
                        className: btn.className || '',
                        dataAction: btn.getAttribute('data-action') || '',
                        dataValue: btn.getAttribute('data-value') || '',
                        ariaLabel: btn.getAttribute('aria-label') || '',
                        title: btn.getAttribute('title') || '',
                        visible: btn.offsetParent !== null,
                        enabled: !btn.disabled,
                        selector: btn.id ? `#${btn.id}` : (btn.className ? `.${btn.className.split(' ')[0]}` : btn.tagName)
                    }));
                }
            """)
            
            return buttons_data
        except Exception as e:
            print(f"❌ Errore ricerca pulsanti: {e}")
            return []
    
    def find_chips(self) -> List[Dict[str, Any]]:
        """Trova tutti i chip/pulsanti di betting"""
        chips = []
        try:
            # Cerca elementi che potrebbero essere chip
            chip_keywords = ['chip', 'bet', '10', '25', '50', '100', '500', '€', '$']
            
            buttons = self.find_all_buttons()
            for btn in buttons:
                text_lower = btn.get('text', '').lower()
                class_lower = btn.get('className', '').lower()
                
                # Verifica se sembra un chip
                is_chip = any(keyword in text_lower or keyword in class_lower for keyword in chip_keywords)
                if is_chip or btn.get('dataValue') or 'chip' in class_lower:
                    chips.append(btn)
            
            return chips
        except Exception as e:
            print(f"❌ Errore ricerca chip: {e}")
            return []
    
    def find_game_actions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Trova pulsanti di azione del gioco (Hit, Stand, ecc.)"""
        actions = {
            'hit': [],
            'stand': [],
            'double': [],
            'split': []
        }
        
        try:
            buttons = self.find_all_buttons()
            
            action_keywords = {
                'hit': ['hit', 'carta', 'card'],
                'stand': ['stand', 'stai', 'stop', 'stay'],
                'double': ['double', 'raddoppia', 'doble'],
                'split': ['split', 'dividi', 'divide']
            }
            
            for btn in buttons:
                text_lower = btn.get('text', '').lower()
                aria_lower = btn.get('ariaLabel', '').lower()
                title_lower = btn.get('title', '').lower()
                data_action = btn.get('dataAction', '').lower()
                
                for action, keywords in action_keywords.items():
                    if (any(kw in text_lower for kw in keywords) or
                        any(kw in aria_lower for kw in keywords) or
                        any(kw in title_lower for kw in keywords) or
                        action in data_action):
                        actions[action].append(btn)
            
            return actions
        except Exception as e:
            print(f"❌ Errore ricerca azioni: {e}")
            return actions
    
    def find_betting_areas(self) -> List[Dict[str, Any]]:
        """Trova aree di betting (canvas, div, ecc.)"""
        areas = []
        try:
            # Cerca canvas
            canvas_count = self.page.locator("canvas").count()
            if canvas_count > 0:
                for i in range(canvas_count):
                    canvas = self.page.locator("canvas").nth(i)
                    box = canvas.bounding_box()
                    if box:
                        areas.append({
                            'type': 'canvas',
                            'index': i,
                            'selector': 'canvas',
                            'position': box,
                            'size': {'width': box['width'], 'height': box['height']}
                        })
            
            # Cerca div/aree con classi comuni
            common_selectors = [
                '.betting-area', '.bet-area', '.bet-zone', '.table-bet',
                '.game-table', '.blackjack-table', '.table'
            ]
            
            for selector in common_selectors:
                count = self.page.locator(selector).count()
                if count > 0:
                    for i in range(count):
                        elem = self.page.locator(selector).nth(i)
                        box = elem.bounding_box()
                        if box:
                            areas.append({
                                'type': 'div',
                                'index': i,
                                'selector': selector,
                                'position': box,
                                'size': {'width': box['width'], 'height': box['height']}
                            })
            
            return areas
        except Exception as e:
            print(f"❌ Errore ricerca aree betting: {e}")
            return []
    
    def generate_report(self) -> Dict[str, Any]:
        """Genera un report completo degli elementi trovati"""
        return {
            'buttons': self.find_all_buttons(),
            'chips': self.find_chips(),
            'actions': self.find_game_actions(),
            'betting_areas': self.find_betting_areas()
        }
    
    def print_report(self):
        """Stampa un report formattato"""
        report = self.generate_report()
        
        print("\n" + "="*70)
        print("🔍 REPORT ELEMENTI TROVATI")
        print("="*70)
        
        print(f"\n📊 PULSANTI TOTALI: {len(report['buttons'])}")
        if report['buttons']:
            print("\n   Primi 10 pulsanti:")
            for btn in report['buttons'][:10]:
                print(f"   - {btn.get('text', '')[:30]:30} | ID: {btn.get('id', 'N/A'):20} | Class: {btn.get('className', 'N/A')[:30]}")
        
        print(f"\n🎲 CHIP TROVATI: {len(report['chips'])}")
        if report['chips']:
            for chip in report['chips']:
                print(f"   - {chip.get('text', '')[:30]:30} | Value: {chip.get('dataValue', 'N/A'):10} | Selector: {chip.get('selector', 'N/A')}")
        
        print(f"\n🎮 AZIONI TROVATE:")
        for action, buttons in report['actions'].items():
            if buttons:
                print(f"   {action.upper()}: {len(buttons)} pulsanti")
                for btn in buttons[:3]:
                    print(f"      - {btn.get('text', '')[:30]:30} | Selector: {btn.get('selector', 'N/A')}")
        
        print(f"\n🎯 AREE BETTING: {len(report['betting_areas'])}")
        for area in report['betting_areas']:
            print(f"   - {area['type']:10} | Selector: {area['selector']:30} | Size: {area['size']['width']}x{area['size']['height']}")
        
        print("\n" + "="*70)















