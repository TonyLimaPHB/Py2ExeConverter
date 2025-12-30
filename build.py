import os
import shutil
import subprocess
import sys
import glob

# ======================================================
# CONFIGURAÇÃO DO BUILD (IGUAL AO PROJETO)
# ======================================================

APP_NAME = "ConversorPythonEXE"
ENTRY_POINT = "main.py"  # chama iniciar_app()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
BUILD_DIR = os.path.join(BASE_DIR, "build")


# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def limpar_tudo():
    """Remove build, dist e QUALQUER .spec"""
    for pasta in (BUILD_DIR, DIST_DIR):
        if os.path.isdir(pasta):
            shutil.rmtree(pasta)
            print(f"🧹 Removido: {pasta}")

    for spec in glob.glob(os.path.join(BASE_DIR, "*.spec")):
        os.remove(spec)
        print(f"🧹 Removido: {spec}")


def encontrar_icone_local():
    """
    Mesmo conceito do projeto:
    - Ícone explícito
    - Caminho absoluto
    """
    for nome in os.listdir(BASE_DIR):
        if nome.lower().endswith(".ico"):
            caminho = os.path.abspath(os.path.join(BASE_DIR, nome))
            return caminho
    return None


def montar_comando_pyinstaller_build():
    """
    MESMA FILOSOFIA DO montar_comando_pyinstaller DO PROJETO
    """
    comando = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",
        "--clean",
        "--noconsole",
        f"--name={APP_NAME}",
    ]

    icone = encontrar_icone_local()
    if icone:
        comando.append(f"--icon={icone}")
        print(f"🎨 Ícone aplicado: {icone}")
    else:
        print("⚠️ Nenhum ícone (.ico) encontrado — build sem ícone")

    comando.append(os.path.abspath(os.path.join(BASE_DIR, ENTRY_POINT)))
    return comando


# ======================================================
# BUILD
# ======================================================

def build():
    print("🚀 BUILD DO CONVERSOR (MODO DEFINITIVO)\n")

    limpar_tudo()

    comando = montar_comando_pyinstaller_build()

    print("\n📦 Comando PyInstaller REAL:")
    print(" ".join(comando))
    print()

    try:
        subprocess.run(
            comando,
            cwd=BASE_DIR,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("\n❌ ERRO NO BUILD")
        print(e)
        sys.exit(1)

    exe_final = os.path.join(DIST_DIR, f"{APP_NAME}.exe")

    if os.path.isfile(exe_final):
        print("\n✅ BUILD FINALIZADO COM SUCESSO")
        print(f"📁 EXE GERADO: {exe_final}")
        print("🧠 Ícone EMBUTIDO no executável")
    else:
        print("\n❌ EXE NÃO GERADO — verifique erros acima")


# ======================================================
# ENTRY
# ======================================================

if __name__ == "__main__":
    build()
