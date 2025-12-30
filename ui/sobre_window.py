import tkinter as tk
from tkinter import ttk

def mostrar_sobre(root):
    texto = """
Conversor Python → EXE

Desenvolvido por Toni Lima

Ferramenta para conversão de scripts Python
e projetos modulares em executáveis (.exe)
utilizando PyInstaller.

Compatível apenas com Windows.

Contato:
Toni Lima
+55 86 98119-2287
"""

    win = tk.Toplevel(root)
    win.title("Sobre")
    win.geometry("600x450")
    win.configure(bg="#f0f0f0")
    win.attributes("-alpha", 0.95)

    label = tk.Label(
        win,
        text=texto,
        font=("Segoe UI", 12),
        bg="#f0f0f0",
        justify="center"
    )
    label.pack(expand=True)

    ttk.Button(win, text="Fechar", command=win.destroy).pack(pady=20)
