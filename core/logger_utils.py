import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "conversoes.log")


def garantir_log():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("=== LOG DE CONVERSÕES ===\n\n")


def registrar_log(titulo, mensagem):
    garantir_log()
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{data}] {titulo}\n")
        f.write(mensagem + "\n")
        f.write("-" * 50 + "\n")
