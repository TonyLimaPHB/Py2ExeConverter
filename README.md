# Py2ExeConverter

## 👨‍💻 Autor / Criador

**Tony Lima**  
📱 WhatsApp: +55 86 98119-2287


![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Windows](https://img.shields.io/badge/Windows-Supported-success)
![PyInstaller](https://img.shields.io/badge/PyInstaller-Used-orange)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Descrição

**Py2ExeConverter** é uma ferramenta profissional para converter **scripts Python** e **projetos modulares completos** em executáveis (`.exe`) para Windows, utilizando **PyInstaller**, com análise inteligente de código e correções automáticas dos problemas mais comuns desse processo.

O projeto vai além de um simples conversor: ele **analisa o código antes do build**, detecta padrões problemáticos e **aplica correções seguras**, garantindo que o EXE final funcione corretamente em uso real.

---

## ✨ Principais Recursos

### 🔧 Conversão
- ✅ Script único (`.py` / `.pyw`)
- ✅ Projeto modular (pastas com vários arquivos)
- ✅ Detecção automática do arquivo principal (`main.py`, `app.py`, etc.)

### 🧠 Análise Inteligente (ANTES da conversão)
Detecta automaticamente métodos problemáticos de acesso a diretórios, como:
- `os.getcwd()`
- `Path.cwd()`
- `__file__`
- `os.path.dirname(os.path.abspath(__file__))`
- Caminhos relativos (`open("arquivo.txt")`, `os.mkdir("logs")`, etc.)

### 🛠️ Correção Automática (Opcional)
- Injeção segura de função **base_dir**
- Neutraliza o problema clássico do `Temp\\_MEIxxxxx` (PyInstaller `--onefile`)
- Garante que arquivos e pastas sejam criados **na pasta real do EXE**
- Sem replace agressivo ou quebra de código

### 🖥️ Suporte a GUI (Tkinter)
- Detecção automática de interface gráfica
- Inclusão forçada dos dados **Tcl/Tk**
- Correção do erro `_tk_data not found`
- Opção automática de ocultar console

### 📦 PyInstaller Robusto
- Hidden-import automático
- Add-data automático
- Suporte a ícone (`.ico`)
- Execução em thread (interface não trava)
- Barra de progresso
- Mensagens claras de sucesso ou erro

### 🎨 Interface
- Interface gráfica em Tkinter
- Tema claro / escuro
- Configurações persistentes
- Logs acessíveis com um clique
- Janela “Sobre”

---

## 🧠 Problemas que o Py2ExeConverter Resolve

| Problema clássico | Resolvido |
|------------------|-----------|
| EXE rodando em `_MEIxxxxx` | ✅ |
| Arquivos criados no local errado | ✅ |
| Tkinter quebrando após conversão | ✅ |
| Hidden imports ausentes | ✅ |
| Projetos grandes não funcionam | ✅ |
| Funciona em `.py` mas falha em `.exe` | ✅ |

---

## 🧩 Estratégia Técnica

- 🔍 **Análise estática de código** (não executa scripts)
- 🧠 Detecção por padrões (regex)
- ⚠️ Aviso ao usuário quando há risco real
- 🔧 Correção via **injeção segura de base_dir**
- ❌ Sem hacks, sem gambiarra, sem replace cego

---

## 📁 Estrutura do Projeto

```text
Py2ExeConverter/
│
├── core/
│   ├── project_utils.py
│   ├── modular_project_utils.py
│   ├── hidden_import_detector.py
│   ├── gui_detector.py
│   ├── pyinstaller_utils.py
│   ├── path_usage_detector.py
│   ├── base_dir_injector.py
│   ├── logger_utils.py
│   └── config_utils.py
│
├── ui/
│   ├── main_window.py
│   ├── sobre_window.py
│   └── theme.py
│
├── build.py
├── main.py
└── README.md
