import os
import subprocess
import threading
import sys

from core.logger_utils import registrar_log


def _detectar_tk_data():
    """
    Detecta automaticamente os diretórios Tcl/Tk do Python
    """
    tcl_dir = os.path.join(sys.base_prefix, "tcl")
    datas = []

    if not os.path.isdir(tcl_dir):
        return datas

    for pasta in os.listdir(tcl_dir):
        caminho = os.path.join(tcl_dir, pasta)
        if os.path.isdir(caminho) and (
            pasta.lower().startswith("tcl") or pasta.lower().startswith("tk")
        ):
            datas.append((caminho, pasta))

    return datas


def montar_comando_pyinstaller(
    arquivo_principal,
    esconder_terminal,
    icone=None,
    add_datas=None,
    hidden_imports=None,
    usa_tkinter=False
):
    """
    Monta comando PyInstaller com suporte COMPLETO a Tkinter
    """

    comando = [
        "pyinstaller",
        "--onefile",
        "--clean",
        "--noconsole" if esconder_terminal else "",
    ]

    if icone:
        comando.append(f"--icon={icone}")

    # hidden-import
    if hidden_imports:
        for mod in hidden_imports:
            comando.append(f"--hidden-import={mod}")

    # add-data do projeto
    if add_datas:
        for origem, destino in add_datas:
            comando.append(f"--add-data={origem}{os.pathsep}{destino}")

    # FIX DEFINITIVO TKINTER
    if usa_tkinter:
        tk_datas = _detectar_tk_data()
        for origem, destino in tk_datas:
            comando.append(f"--add-data={origem}{os.pathsep}{destino}")

    comando.append(arquivo_principal)

    return [c for c in comando if c]


def _executar_pyinstaller(
    comando,
    cwd,
    contexto,
    gui_info,
    hidden_imports,
    on_finish
):
    registrar_log(
        "INÍCIO",
        f"Tipo: {contexto}\n"
        f"{gui_info}\n"
        f"Comando:\n{' '.join(comando)}"
    )

    try:
        subprocess.run(comando, check=True, cwd=cwd)
        sucesso = True
        erro = None

        registrar_log(
            "SUCESSO",
            f"Build concluído com sucesso.\nSaída: {os.path.join(cwd, 'dist')}"
        )

    except Exception as e:
        sucesso = False
        erro = str(e)

        registrar_log(
            "ERRO",
            f"Falha na conversão.\nErro:\n{erro}"
        )

    if on_finish:
        on_finish(sucesso, erro, cwd)


def executar_pyinstaller_thread(
    comando,
    cwd,
    contexto,
    gui_info,
    hidden_imports,
    on_finish
):
    threading.Thread(
        target=_executar_pyinstaller,
        args=(comando, cwd, contexto, gui_info, hidden_imports, on_finish),
        daemon=True
    ).start()
