import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


# ================================
# Funções principais
# ================================

def encontrar_arquivo_principal(diretorio):
    """Procura o arquivo principal do projeto (main.py, app.py, etc.)."""
    candidatos = ["main.py", "app.py", "__main__.py", "run.py"]
    for candidato in candidatos:
        caminho = os.path.join(diretorio, candidato)
        if os.path.isfile(caminho):
            return caminho
    return None


def converter_para_exe(arquivo_entrada, esconder_terminal, arquivo_icone=None):
    """Converte o arquivo Python para executável (.exe) usando PyInstaller."""
    comando = [
        "pyinstaller",
        "--onefile",
        "--noconsole" if esconder_terminal else "",
        f"--icon={arquivo_icone}" if arquivo_icone else "",
        "--clean",
        arquivo_entrada
    ]
    comando = [arg for arg in comando if arg]

    try:
        subprocess.run(comando, check=True, cwd=os.path.dirname(arquivo_entrada))
        messagebox.showinfo(
            "Sucesso!",
            f"Arquivo convertido com sucesso!\n\n"
            f"Executável gerado em: {os.path.join(os.path.dirname(arquivo_entrada), 'dist')}"
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Falha ao converter:\n{e}")
    except FileNotFoundError:
        messagebox.showerror("Erro", "PyInstaller não encontrado!\nInstale com: pip install pyinstaller")


def converter_projeto_para_exe(diretorio_projeto):
    """Converte um projeto modular (diretório com vários arquivos Python) para executável."""
    arquivo_principal = encontrar_arquivo_principal(diretorio_projeto)
    if not arquivo_principal:
        messagebox.showerror(
            "Erro",
            "Arquivo principal não encontrado!\n"
            "Certifique-se de ter um 'main.py', 'app.py' ou '__main__.py' na pasta selecionada."
        )
        return

    esconder_terminal = messagebox.askyesno(
        "Configuração",
        "Esconder o terminal ao executar?\n(Recomendado para aplicações GUI)"
    )

    usar_icone = messagebox.askyesno("Configuração", "Deseja adicionar um ícone personalizado (.ico)?")
    arquivo_icone = None
    if usar_icone:
        arquivo_icone = filedialog.askopenfilename(
            title="Selecione o arquivo de ícone (.ico)",
            filetypes=[("Ícones", "*.ico"), ("Todos os arquivos", "*.*")]
        )

    comando = [
        "pyinstaller",
        "--onefile",
        "--noconsole" if esconder_terminal else "",
        f"--icon={arquivo_icone}" if arquivo_icone else "",
        "--clean",
        arquivo_principal
    ]
    comando = [arg for arg in comando if arg]

    try:
        subprocess.run(comando, check=True, cwd=diretorio_projeto)
        messagebox.showinfo(
            "Sucesso!",
            f"Projeto convertido com sucesso!\n\n"
            f"Executável gerado em: {os.path.join(diretorio_projeto, 'dist')}"
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Falha ao converter:\n{e}")
    except FileNotFoundError:
        messagebox.showerror("Erro", "PyInstaller não encontrado!\nInstale com: pip install pyinstaller")


def iniciar_conversao():
    tipo_projeto = var_tipo.get()

    if tipo_projeto == "unico":
        arquivo_entrada = filedialog.askopenfilename(
            title="Selecione o arquivo Python (.py ou .pyw)",
            filetypes=[("Arquivos Python", "*.py *.pyw"), ("Todos os arquivos", "*.*")]
        )
        if not arquivo_entrada:
            return

        esconder_terminal = messagebox.askyesno("Configuração", "Esconder o terminal ao executar?")

        usar_icone = messagebox.askyesno("Configuração", "Deseja adicionar um ícone personalizado (.ico)?")
        arquivo_icone = None
        if usar_icone:
            arquivo_icone = filedialog.askopenfilename(
                title="Selecione o arquivo de ícone (.ico)",
                filetypes=[("Ícones", "*.ico"), ("Todos os arquivos", "*.*")]
            )

        converter_para_exe(arquivo_entrada, esconder_terminal, arquivo_icone)

    elif tipo_projeto == "modular":
        diretorio_projeto = filedialog.askdirectory(title="Selecione a pasta do projeto")
        if not diretorio_projeto:
            return
        converter_projeto_para_exe(diretorio_projeto)


# ================================
# Função para Janela "Sobre"
# ================================

def mostrar_sobre():
    """Exibe uma janela separada para o 'Sobre' com texto centralizado."""
    sobre = """
    Conversor Python → EXE

    Desenvolvido por Toni Lima

    Este projeto visa facilitar a conversão de scripts Python 
    e projetos completos em arquivos executáveis (.exe) utilizando 
    o PyInstaller. **Este projeto é apenas para conversão em sistemas Windows.**

    A ferramenta suporta diferentes configurações, 
    como esconder o terminal e personalizar o ícone do executável.

    Contato:
    Toni Lima
    +5586981192287
    """

    # Criar uma janela "Sobre"
    sobre_window = tk.Toplevel(root)
    sobre_window.title("Sobre o Projeto")

    # Sincronizando posição e tamanho com a janela principal
    x = root.winfo_x() + (root.winfo_width() // 2) - 250
    y = root.winfo_y() + (root.winfo_height() // 2) - 200
    sobre_window.geometry(f"600x450+{x}+{y}")  # Aumentei a janela para 600x450

    # Tornando o fundo um pouco transparente
    sobre_window.configure(bg="#f0f0f0")
    sobre_window.attributes("-alpha", 0.95)

    sobre_label = tk.Label(sobre_window, text=sobre, font=("Segoe UI", 12), bg="#f0f0f0", justify="center",
                           anchor="center")
    sobre_label.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza o texto

    # Adicionar o botão "Fechar"
    btn_fechar = ttk.Button(sobre_window, text="Fechar", command=sobre_window.destroy, style="RoundedButton.TButton")
    btn_fechar.pack(pady=20)


# ================================
# Configuração da Janela Principal
# ================================

root = tk.Tk()
root.title("Conversor Python → EXE")
root.geometry("600x400")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

style = ttk.Style()
style.theme_use('clam')

# Estilo customizado para botões
style.configure("RoundedButton.TButton",
                font=("Segoe UI", 12),
                padding=10,
                background="#4CAF50",
                foreground="white",
                borderwidth=0,
                focusthickness=3,
                focuscolor="none")
style.map("RoundedButton.TButton",
          background=[("active", "#45a049")])

# Título
title_label = tk.Label(root, text="Conversor Python para Executável", font=("Segoe UI", 18, "bold"), bg="#f5f5f5",
                       fg="#333")
title_label.pack(pady=20)

# Frame para opções
frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(pady=10)

var_tipo = tk.StringVar(value="unico")

rb1 = ttk.Radiobutton(frame, text="Script Único (.py / .pyw)", variable=var_tipo, value="unico", style="TRadiobutton")
rb1.grid(row=0, column=0, sticky="w", pady=5)

rb2 = ttk.Radiobutton(frame, text="Projeto Modular (Pasta com vários arquivos)", variable=var_tipo, value="modular",
                      style="TRadiobutton")
rb2.grid(row=1, column=0, sticky="w", pady=5)

# Botão de início
botao = ttk.Button(root, text="Selecionar e Converter", command=iniciar_conversao, style="RoundedButton.TButton")
botao.pack(pady=30)

# Botão "Sobre"
botao_sobre = ttk.Button(root, text="Sobre", command=mostrar_sobre, style="RoundedButton.TButton")
botao_sobre.pack(pady=5)

# Rodapé
footer_label = tk.Label(root, text="© 2025 Conversor Python para EXE", font=("Segoe UI", 10), bg="#f5f5f5", fg="#aaa")
footer_label.pack(side="bottom", pady=10)

# Inicia a interface
root.mainloop()
