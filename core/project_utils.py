import os

def encontrar_arquivo_principal(diretorio):
    """Procura o arquivo principal do projeto."""
    candidatos = ["main.py", "app.py", "__main__.py", "run.py"]
    for nome in candidatos:
        caminho = os.path.join(diretorio, nome)
        if os.path.isfile(caminho):
            return caminho
    return None
