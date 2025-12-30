import re

GUI_KEYWORDS = [
    "tkinter",
    "customtkinter",
    "PyQt5",
    "PyQt6",
    "PySide2",
    "PySide6",
    "wx",
    "kivy",
    "dearpygui"
]


def detectar_gui(arquivo_py):
    """
    Analisa o arquivo Python e verifica se ele utiliza alguma
    biblioteca gráfica conhecida.
    """
    try:
        with open(arquivo_py, "r", encoding="utf-8", errors="ignore") as f:
            conteudo = f.read()
    except Exception:
        return False, None

    for lib in GUI_KEYWORDS:
        padrao = rf"(import\s+{lib}|from\s+{lib}\s+import)"
        if re.search(padrao, conteudo):
            return True, lib

    return False, None
