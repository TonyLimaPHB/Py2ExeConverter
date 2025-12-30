import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.project_utils import encontrar_arquivo_principal
from core.modular_project_utils import detectar_dados
from core.hidden_import_detector import detectar_hidden_imports
from core.pyinstaller_utils import executar_pyinstaller_thread, montar_comando_pyinstaller
from core.gui_detector import detectar_gui
from core.logger_utils import LOG_FILE
from core.config_utils import carregar_config, salvar_config
from core.path_detector import detectar_problemas_caminho
from ui.sobre_window import mostrar_sobre
from ui.theme import aplicar_tema


def iniciar_app():
    config = carregar_config()

    root = tk.Tk()
    root.title("Conversor Python → EXE")
    root.geometry("720x620")
    root.resizable(False, False)

    aplicar_tema(root, config["tema"])

    # ======================================================
    # FUNÇÕES AUXILIARES
    # ======================================================

    def alternar_tema():
        config["tema"] = "light" if config["tema"] == "dark" else "dark"
        salvar_config(config)
        aplicar_tema(root, config["tema"])

    def abrir_log():
        if not os.path.isfile(LOG_FILE):
            messagebox.showinfo("Log", "Nenhum log encontrado.")
            return
        subprocess.Popen(["notepad.exe", LOG_FILE])

    def mostrar_progresso():
        win = tk.Toplevel(root)
        win.title("Convertendo...")
        win.geometry("420x160")
        win.resizable(False, False)
        win.transient(root)
        win.grab_set()

        ttk.Label(
            win,
            text="Convertendo para executável...\nAguarde.",
            font=("Segoe UI", 11)
        ).pack(pady=20)

        barra = ttk.Progressbar(win, mode="indeterminate", length=320)
        barra.pack(pady=10)
        barra.start(10)

        return win

    def finalizar_conversao(win, sucesso, erro, cwd):
        win.destroy()
        if sucesso:
            messagebox.showinfo(
                "Sucesso",
                f"Executável gerado com sucesso!\n\nLocal:\n{os.path.join(cwd, 'dist')}"
            )
        else:
            messagebox.showerror(
                "Erro",
                erro or "Erro desconhecido durante a conversão."
            )

    # ======================================================
    # CONVERSÃO
    # ======================================================

    def iniciar_conversao():
        tipo = var_tipo.get()

        # -------------------------------
        # SCRIPT ÚNICO
        # -------------------------------
        if tipo == "unico":
            arquivo_principal = filedialog.askopenfilename(
                title="Selecione o arquivo Python",
                initialdir=os.path.dirname(config["ultimo_arquivo"]) if config["ultimo_arquivo"] else None,
                filetypes=[("Python", "*.py *.pyw")]
            )
            if not arquivo_principal:
                return

            cwd = os.path.dirname(arquivo_principal)
            add_datas = None
            hidden_imports = None

        # -------------------------------
        # PROJETO MODULAR
        # -------------------------------
        else:
            pasta = filedialog.askdirectory(
                title="Selecione o projeto",
                initialdir=config["ultima_pasta"] if config["ultima_pasta"] else None
            )
            if not pasta:
                return

            arquivo_principal = encontrar_arquivo_principal(pasta)
            if not arquivo_principal:
                messagebox.showerror(
                    "Erro",
                    "Arquivo principal não encontrado (main.py, app.py, etc.)"
                )
                return

            cwd = pasta
            add_datas = detectar_dados(cwd)
            hidden_imports = detectar_hidden_imports(cwd)

            # -------- VERIFICA CAMINHOS (EXE) --------
            problemas = detectar_problemas_caminho(cwd)
            if problemas:
                aviso = (
                    "⚠️ ATENÇÃO\n\n"
                    "Este projeto utiliza caminhos relativos como:\n"
                    "os.getcwd(), __file__ ou Path.cwd()\n\n"
                    "Em executáveis isso pode causar problemas de acesso a arquivos.\n\n"
                    "Recomendado usar:\n"
                    "get_base_dir() baseado em sys.executable.\n\n"
                    "Deseja continuar mesmo assim?"
                )
                if not messagebox.askyesno("Aviso de Caminhos", aviso):
                    return

        # -------------------------------
        # DETECÇÃO DE GUI
        # -------------------------------
        usa_gui, lib_gui = detectar_gui(arquivo_principal)
        info_gui = f"GUI detectada: {lib_gui}" if usa_gui else "Nenhuma GUI detectada"

        esconder_terminal = messagebox.askyesno(
            "Configuração",
            f"{info_gui}\n\nDeseja esconder o terminal?",
            default=messagebox.YES if usa_gui else messagebox.NO
        )

        # -------------------------------
        # ÍCONE
        # -------------------------------
        usar_icone = messagebox.askyesno(
            "Configuração",
            "Deseja adicionar um ícone (.ico)?"
        )

        icone = config["ultimo_icone"]
        if usar_icone:
            icone = filedialog.askopenfilename(
                title="Selecione o ícone",
                initialdir=os.path.dirname(icone) if icone else None,
                filetypes=[("Ícones", "*.ico")]
            )

        # -------------------------------
        # COMANDO PYINSTALLER
        # -------------------------------
        comando = montar_comando_pyinstaller(
            arquivo_principal,
            esconder_terminal,
            icone,
            add_datas=add_datas,
            hidden_imports=hidden_imports,
            usa_tkinter=usa_gui
        )

        # -------------------------------
        # SALVA CONFIG
        # -------------------------------
        config.update({
            "tipo_projeto": tipo,
            "ultimo_arquivo": arquivo_principal if tipo == "unico" else config["ultimo_arquivo"],
            "ultima_pasta": cwd if tipo == "modular" else config["ultima_pasta"],
            "ultimo_icone": icone,
            "esconder_terminal": esconder_terminal
        })
        salvar_config(config)

        # -------------------------------
        # THREAD + PROGRESSO
        # -------------------------------
        win = mostrar_progresso()

        executar_pyinstaller_thread(
            comando,
            cwd,
            "Projeto Modular" if tipo == "modular" else "Script Único",
            info_gui,
            hidden_imports,
            lambda sucesso, erro, c: root.after(
                0, finalizar_conversao, win, sucesso, erro, c
            )
        )

    # ======================================================
    # INTERFACE
    # ======================================================

    ttk.Label(
        root,
        text="Conversor Python para Executável",
        style="Title.TLabel"
    ).pack(pady=15)

    ttk.Label(
        root,
        text="Tipo de Conversão",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=(10, 5))

    frame = ttk.Frame(root)
    frame.pack(pady=10)

    var_tipo = tk.StringVar(value=config.get("tipo_projeto", "unico"))

    ttk.Radiobutton(
        frame,
        text="Script Único (.py / .pyw)",
        variable=var_tipo,
        value="unico"
    ).pack(anchor="w", pady=6)

    ttk.Radiobutton(
        frame,
        text="Projeto Modular (Pasta)",
        variable=var_tipo,
        value="modular"
    ).pack(anchor="w", pady=6)

    ttk.Button(
        root,
        text="Selecionar e Converter",
        command=iniciar_conversao,
        style="RoundedButton.TButton"
    ).pack(pady=25)

    ttk.Button(
        root,
        text="Alternar Tema",
        command=alternar_tema,
        style="RoundedButton.TButton"
    ).pack(pady=5)

    ttk.Button(
        root,
        text="Abrir Log",
        command=abrir_log,
        style="RoundedButton.TButton"
    ).pack(pady=5)

    ttk.Button(
        root,
        text="Sobre",
        command=lambda: mostrar_sobre(root),
        style="RoundedButton.TButton"
    ).pack(pady=5)

    ttk.Label(
        root,
        text="© 2025 Conversor Python para EXE"
    ).pack(side="bottom", pady=10)

    root.mainloop()
