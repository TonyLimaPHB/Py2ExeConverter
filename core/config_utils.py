import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "tipo_projeto": "unico",
    "ultimo_arquivo": "",
    "ultima_pasta": "",
    "ultimo_icone": "",
    "esconder_terminal": True,
    "tema": "dark"
}


def carregar_config():
    if not os.path.isfile(CONFIG_FILE):
        salvar_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG.copy()


def salvar_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
