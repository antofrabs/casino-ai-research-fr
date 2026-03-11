#!/usr/bin/env python3
"""
💻 Code Editor - Editor di codice integrato
============================================

Permette di modificare il codice direttamente dall'interfaccia web
"""
import streamlit as st
from pathlib import Path
import os
import importlib
import sys

def show_code_editor():
    """Mostra l'editor di codice"""
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.header("💻 Editor di Codice")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.warning("⚠️ **ATTENZIONE**: Le modifiche vengono salvate direttamente sui file. Fai attenzione!")
    
    # Seleziona file da modificare
    project_root = Path(__file__).parent.parent.parent
    
    # Cerca tutti i file Python
    python_files = []
    for root, dirs, files in os.walk(project_root):
        # Escludi directory comuni
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                rel_path = file_path.relative_to(project_root)
                python_files.append(str(rel_path))
    
    python_files.sort()
    
    # Selezione file
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_file = st.selectbox(
            "📁 Seleziona file da modificare:",
            python_files,
            key="code_editor_file"
        )
    
    with col2:
        if st.button("🔄 Ricarica File", use_container_width=True):
            if 'file_content' in st.session_state:
                del st.session_state.file_content
            st.rerun()
    
    if selected_file:
        file_path = project_root / selected_file
        
        # Leggi file
        if 'file_content' not in st.session_state or st.session_state.get('current_file') != selected_file:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    st.session_state.file_content = f.read()
                st.session_state.current_file = selected_file
            except Exception as e:
                st.error(f"❌ Errore lettura file: {e}")
                return
        
        # Editor di codice
        st.markdown("### 📝 Contenuto File")
        
        # Usa streamlit-ace se disponibile, altrimenti textarea
        try:
            from streamlit_ace import st_ace
            
            edited_code = st_ace(
                value=st.session_state.file_content,
                language='python',
                theme='monokai',
                key=f"ace_{selected_file}",
                font_size=14,
                height=600,
                wrap=True,
                show_gutter=True,
                show_print_margin=True,
                auto_update=False
            )
        except ImportError:
            # Fallback a textarea normale
            st.info("💡 Installa `streamlit-ace` per un editor migliore: `pip install streamlit-ace`")
            edited_code = st.text_area(
                "Codice:",
                value=st.session_state.file_content,
                height=600,
                key=f"textarea_{selected_file}"
            )
        
        # Pulsanti di azione
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Salva File", type="primary", use_container_width=True):
                try:
                    # Backup del file originale
                    backup_path = file_path.with_suffix(f'.py.backup')
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(st.session_state.file_content)
                    
                    # Salva nuovo contenuto
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(edited_code)
                    
                    # Aggiorna session state
                    st.session_state.file_content = edited_code
                    
                    st.success(f"✅ File salvato! Backup creato: {backup_path.name}")
                    
                    # Ricarica modulo se è un modulo Python
                    if selected_file.startswith('src/'):
                        module_path = selected_file.replace('/', '.').replace('.py', '')
                        try:
                            if module_path in sys.modules:
                                importlib.reload(sys.modules[module_path])
                                st.info(f"🔄 Modulo {module_path} ricaricato!")
                        except Exception as e:
                            st.warning(f"⚠️ Impossibile ricaricare modulo: {e}")
                    
                except Exception as e:
                    st.error(f"❌ Errore salvataggio: {e}")
        
        with col2:
            if st.button("🔄 Ripristina", use_container_width=True):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        st.session_state.file_content = f.read()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Errore ripristino: {e}")
        
        with col3:
            if st.button("📋 Backup", use_container_width=True):
                backup_files = list(file_path.parent.glob(f"{file_path.stem}.py.backup*"))
                if backup_files:
                    st.info(f"📦 Backup disponibili: {len(backup_files)}")
                    for backup in backup_files[-5:]:  # Ultimi 5
                        st.text(backup.name)
                else:
                    st.info("📦 Nessun backup disponibile")
        
        with col4:
            if st.button("❌ Chiudi Editor", use_container_width=True):
                st.session_state.show_code_editor = False
                if 'file_content' in st.session_state:
                    del st.session_state.file_content
                if 'current_file' in st.session_state:
                    del st.session_state.current_file
                st.rerun()
        
        # Info file
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 File", selected_file)
        with col2:
            file_size = file_path.stat().st_size
            st.metric("📊 Dimensione", f"{file_size:,} bytes")
        with col3:
            lines = len(st.session_state.file_content.split('\n'))
            st.metric("📝 Righe", lines)
        
        # Anteprima modifiche
        if edited_code != st.session_state.file_content:
            st.markdown("### 🔍 Anteprima Modifiche")
            st.info("⚠️ Hai modifiche non salvate!")
            
            # Mostra differenze (semplificato)
            original_lines = st.session_state.file_content.split('\n')
            edited_lines = edited_code.split('\n')
            
            if len(original_lines) != len(edited_lines):
                st.write(f"**Righe**: {len(original_lines)} → {len(edited_lines)}")
            
            # Conta caratteri
            original_chars = len(st.session_state.file_content)
            edited_chars = len(edited_code)
            if original_chars != edited_chars:
                st.write(f"**Caratteri**: {original_chars:,} → {edited_chars:,}")
