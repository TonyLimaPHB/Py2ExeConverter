import os

DATA_EXTENSIONS = (
    ".json", ".ini", ".cfg", ".txt",
    ".png", ".jpg", ".jpeg", ".ico",
    ".csv"
)


def detectar_pastas_python(raiz):
    pastas = set()

    for root, dirs, files in os.walk(raiz):
        if any(f.endswith(".py") for f in files):
            pastas.add(root)

    return list(pastas)


def detectar_dados(raiz):
    arquivos = []

    for root, _, files in os.walk(raiz):
        for f in files:
            if f.lower().endswith(DATA_EXTENSIONS):
                caminho = os.path.join(root, f)
                destino = os.path.relpath(root, raiz)
                arquivos.append((caminho, destino))

    return arquivos
