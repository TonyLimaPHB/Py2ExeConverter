INJECAO = """# === AUTO-INJETADO PELO CONVERSOR ===
import sys
import os

def __exe_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

os.chdir(__exe_base_dir())
# === FIM DA INJEÇÃO ===

"""


def injetar_base_dir(caminho_script):
    with open(caminho_script, "r", encoding="utf-8", errors="ignore") as f:
        conteudo = f.read()

    if "__exe_base_dir" in conteudo:
        return False  # já corrigido

    novo = INJECAO + conteudo

    with open(caminho_script, "w", encoding="utf-8") as f:
        f.write(novo)

    return True
