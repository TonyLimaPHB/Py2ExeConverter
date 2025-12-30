import os


def gerar_spec(
    nome_app,
    arquivo_principal,
    pasta_projeto,
    esconder_terminal,
    icone,
    hidden_imports,
    datas
):
    """
    Gera um arquivo .spec customizado para projetos modulares.
    """
    spec_path = os.path.join(pasta_projeto, f"{nome_app}.spec")

    hidden_imports = hidden_imports or []
    datas = datas or []

    datas_formatadas = []
    for origem, destino in datas:
        datas_formatadas.append(f"('{origem}', '{destino}')")

    spec_conteudo = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{arquivo_principal}'],
    pathex=['{pasta_projeto}'],
    binaries=[],
    datas=[{', '.join(datas_formatadas)}],
    hiddenimports={hidden_imports},
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{nome_app}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console={not esconder_terminal},
    icon='{icone}' if '{icone}' else None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='{nome_app}'
)
"""

    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(spec_conteudo.strip())

    return spec_path
