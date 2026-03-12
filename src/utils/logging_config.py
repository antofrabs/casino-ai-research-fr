#!/usr/bin/env python3
"""
📝 Logging centralizzato per Casino AI Research
================================================

Crea un file di log con eventi ed errori principali.
Su Streamlit Cloud il filesystem è effimero ma il log è comunque utile
per diagnostica durante la sessione.
"""
import logging
from pathlib import Path


def setup_logging() -> logging.Logger:
    """Configura il logging di base e restituisce un logger di modulo."""
    # Cartella logs nella root del progetto
    project_root = Path(__file__).parent.parent
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "app.log"

    # Configurazione base solo la prima volta
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

    logger = logging.getLogger("casino_ai")
    logger.info("🔄 Logger inizializzato. Scrittura su %s", log_file)
    return logger


def get_logger(name: str) -> logging.Logger:
    """Restituisce un logger figlio con nome dato."""
    parent = setup_logging()
    return parent.getChild(name)

