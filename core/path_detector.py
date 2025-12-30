import os

PADROES_RISCO = [
    "os.getcwd(",
    "Path.cwd(",
    "__file__"
]

def detectar_problemas_caminho(pasta_projeto):
    encontrados = []

    for root, _, files in os.walk(pasta_projeto):
        for file in files:
            if file.endswith(".py"):
                caminho = os.path.join(root, file)
                try:
                    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                        conteudo = f.read()
                        for padrao in PADROES_RISCO:
                            if padrao in conteudo:
                                encontrados.append((caminho, padrao))
                except Exception:
                    pass

    return encontrados
