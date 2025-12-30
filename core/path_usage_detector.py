import os
import re

# =============================================
# PADRÕES DE ACESSO A DIRETÓRIOS (ANTES DO EXE)
# =============================================

PADROES = {
    # ALTO RISCO (quebra quase sempre)
    "os.getcwd": {
        "regex": r"os\.getcwd\s*\(",
        "risco": "ALTO",
        "descricao": "Uso de os.getcwd()"
    },
    "Path.cwd": {
        "regex": r"Path\.cwd\s*\(",
        "risco": "ALTO",
        "descricao": "Uso de Path.cwd()"
    },

    # MÉDIO RISCO
    "__file__": {
        "regex": r"__file__",
        "risco": "MÉDIO",
        "descricao": "Uso direto de __file__"
    },
    "dirname_abspath_file": {
        "regex": r"os\.path\.dirname\s*\(\s*os\.path\.abspath\s*\(\s*__file__\s*\)\s*\)",
        "risco": "MÉDIO",
        "descricao": "os.path.dirname(os.path.abspath(__file__))"
    },
    "sys.argv": {
        "regex": r"sys\.argv\s*\[\s*0\s*\]",
        "risco": "MÉDIO",
        "descricao": "Uso de sys.argv[0]"
    },

    # BAIXO RISCO (informativo)
    "relative_open": {
        "regex": r"open\s*\(\s*[\"'][^/\\]",
        "risco": "BAIXO",
        "descricao": "open() com caminho relativo"
    },
    "relative_mkdir": {
        "regex": r"os\.mkdir\s*\(\s*[\"'][^/\\]",
        "risco": "BAIXO",
        "descricao": "os.mkdir() com caminho relativo"
    },
    "relative_makedirs": {
        "regex": r"os\.makedirs\s*\(\s*[\"'][^/\\]",
        "risco": "BAIXO",
        "descricao": "os.makedirs() com caminho relativo"
    }
}


def detectar_metodos_caminho(pasta_projeto):
    """
    Escaneia o projeto e detecta métodos de acesso a diretórios
    Retorna lista estruturada
    """
    encontrados = []

    for root, _, files in os.walk(pasta_projeto):
        for file in files:
            if not file.endswith(".py"):
                continue

            caminho = os.path.join(root, file)

            try:
                with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                    conteudo = f.read()

                for chave, info in PADROES.items():
                    if re.search(info["regex"], conteudo):
                        encontrados.append({
                            "arquivo": caminho,
                            "metodo": chave,
                            "descricao": info["descricao"],
                            "risco": info["risco"]
                        })

            except Exception:
                pass

    return encontrados
