# 🧾 PDF Renamer — Renomeador Automático de PDFs

Um utilitário em **Python 3.14** que lê e renomeia arquivos PDF automaticamente, extraindo informações do conteúdo (texto ou imagem) para gerar nomes de arquivos organizados e padronizados.

O projeto suporta:
- PDFs baseados em texto
- PDFs baseados em imagem (via OCR com **Tesseract**)
- Processamento em lote: basta selecionar uma pasta com os arquivos e o programa faz o resto 🚀

---

## ⚙️ Tecnologias Utilizadas

| Biblioteca | Função Principal |
|-------------|------------------|
| `PyMuPDF` | Leitura e extração de texto de PDFs |
| `pdf2image` | Conversão de páginas em imagem (para OCR) |
| `pytesseract` | Reconhecimento de texto em PDFs de imagem |
| `Pillow` | Manipulação de imagens |
| `pyinstaller` | Geração de executável |
| `macholib`, `altgraph` | Dependências internas do PyInstaller |
| `packaging`, `setuptools` | Instalação e empacotamento |

---

## 🧠 Como Funciona

1. O programa solicita que você selecione uma **pasta contendo arquivos PDF**.  
2. Para cada arquivo:
   - Lê o conteúdo (texto ou imagem).
   - Extrai informações relevantes (como nome, número, data, etc.).
   - Gera um **novo nome de arquivo**.
3. Renomeia automaticamente os arquivos na pasta.

Tudo de forma simples e automatizada ✅

---

## 💻 Como Usar

### 🔹 Passo 1 — Baixar e Executar

Baixe o arquivo executável (`.exe`, `.app` ou binário Linux) correspondente ao seu sistema operacional.

1. Execute o programa.
2. Uma janela se abrirá pedindo para selecionar a **pasta com PDFs**.
3. O programa processará todos os arquivos, exibindo logs ou mensagens de status.

Os arquivos renomeados serão salvos na **mesma pasta original**.

---

## 🧩 Rodando o Projeto Localmente

Caso deseje rodar o código Python em vez do executável:

### 1. Clone o repositório

```bash
git clone https://github.com/digitaku/renomeador-pdf.git
cd renomeador-pdf
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o programa

```bash
python main.py
```

---

## 🏗️ Gerando o Executável

Para empacotar o programa e gerar um arquivo `.exe` (Windows) ou binário (Linux/macOS), use o **PyInstaller**:

```bash
pyinstaller --name "renomeador-pdf" --onefile --noconsole --add-binary "tesseract/*;tesseract" --add-data "tesseract/tessdata;tesseract/tessdata" main.py
```

ou utilize o comando para gerar um executavel que abre o console

```bash
pyinstaller --name "renomeador-pdf-console" --onefile --add-binary "tesseract/*;tesseract" --add-data "tesseract/tessdata;tesseract/tessdata" main.py
```

O executável será criado na pasta `dist/`.

---

## 📦 Atualizando Dependências

Sempre que adicionar uma nova biblioteca, atualize o `requirements.txt` com:

```bash
pip freeze > requirements.txt
```

---

## 🧰 Estrutura do Projeto (sugerida)

```
renomeador-pdf/
├── main.py
├── requirements.txt
├── tesseract/
│   ├── tesseract
│   ├── tesseract.exe
│   └── tessdata/
├── LICENCE
└── README.md
```

---

## 🤝 Contribuidores

Agradecimentos especiais a todos que ajudaram a construir o projeto 💙  

| [<img src="https://avatars.githubusercontent.com/u/50982572?v=4" width="80" height="80" style="border-radius:50%">](https://github.com/digitaku) |
|:--:|
| [@digitaku](https://github.com/digitaku) |

---

## 🧾 Licença

Este projeto é distribuído sob a licença **MIT**.  
Sinta-se à vontade para usar, modificar e contribuir!
