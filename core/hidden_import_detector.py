import ast
import os

IGNORAR = {
    "os", "sys", "tkinter", "subprocess",
    "threading", "json", "re", "time",
    "logging", "pathlib"
}


def detectar_hidden_imports(raiz_projeto):
    encontrados = set()

    for root, _, files in os.walk(raiz_projeto):
        for file in files:
            if not file.endswith(".py"):
                continue

            caminho = os.path.join(root, file)

            try:
                with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                    arvore = ast.parse(f.read(), filename=caminho)
            except Exception:
                continue

            for node in ast.walk(arvore):
                # import x
                if isinstance(node, ast.Import):
                    for n in node.names:
                        mod = n.name.split(".")[0]
                        if mod not in IGNORAR:
                            encontrados.add(mod)

                # from x import y
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        mod = node.module.split(".")[0]
                        if mod not in IGNORAR:
                            encontrados.add(mod)

                # importlib.import_module("x")
                elif isinstance(node, ast.Call):
                    if hasattr(node.func, "attr") and node.func.attr == "import_module":
                        if node.args and isinstance(node.args[0], ast.Constant):
                            mod = str(node.args[0].value).split(".")[0]
                            encontrados.add(mod)

                    # __import__("x")
                    if hasattr(node.func, "id") and node.func.id == "__import__":
                        if node.args and isinstance(node.args[0], ast.Constant):
                            mod = str(node.args[0].value).split(".")[0]
                            encontrados.add(mod)

    return sorted(encontrados)
