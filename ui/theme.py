from tkinter import ttk

DARK = {
    "bg": "#1e1e1e",
    "bg_secondary": "#252526",
    "fg": "#d4d4d4",
    "accent": "#0a84ff",
    "button": "#2d2d30",
    "button_hover": "#3a3a3d",
    "progress": "#0a84ff",
}

LIGHT = {
    "bg": "#f5f5f5",
    "bg_secondary": "#ffffff",
    "fg": "#1f1f1f",
    "accent": "#0a84ff",
    "button": "#e0e0e0",
    "button_hover": "#d0d0d0",
    "progress": "#0a84ff",
}


def aplicar_tema(root, tema="dark"):
    cores = DARK if tema == "dark" else LIGHT

    style = ttk.Style(root)
    style.theme_use("clam")

    root.configure(bg=cores["bg"])

    style.configure("TFrame", background=cores["bg"])
    style.configure("TLabel", background=cores["bg"], foreground=cores["fg"])
    style.configure(
        "Title.TLabel",
        font=("Segoe UI", 18, "bold"),
        background=cores["bg"],
        foreground=cores["fg"]
    )

    style.configure(
        "TRadiobutton",
        background=cores["bg"],
        foreground=cores["fg"]
    )

    style.configure(
        "RoundedButton.TButton",
        background=cores["button"],
        foreground=cores["fg"],
        padding=10,
        borderwidth=0
    )

    style.map(
        "RoundedButton.TButton",
        background=[("active", cores["button_hover"])]
    )

    style.configure(
        "TProgressbar",
        troughcolor=cores["bg_secondary"],
        background=cores["progress"]
    )
