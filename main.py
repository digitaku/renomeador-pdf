import os
import re
import fitz  # PyMuPDF
import pytesseract
from tkinter import filedialog, Tk
import os
import sys
import pytesseract
from PIL import Image
import io

if getattr(sys, 'frozen', False):
    app_dir = sys._MEIPASS  # pasta temporária usada pelo PyInstaller
    tipo_tesseract = "tesseract.exe" if os.name == 'nt' else "tesseract"
    tesseract_path = os.path.join(app_dir, "tesseract", tipo_tesseract)
else:
    # Caminho padrão do sistema (para rodar no ambiente de desenvolvimento)
    if os.name == 'nt':  # Windows
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    else:
        tesseract_path = "/opt/homebrew/bin/tesseract" # Mac m3 (Apple Silicon) brew

def escolher_pasta():
    root = Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title="Selecione a pasta com PDFs")
    return pasta

# --- Configurações ---
PASTA = escolher_pasta()

# Regex para detectar algo no texto (exemplo: CPF)
PADRAO_MATRICULA =re.compile( r"""
    (?:                                 # Grupo não capturante
        (?:TD|TR|TO)_[^-]*-?            # Prefixo TD_/TR_/TO_
        (\d{6,10})                      # ← matrícula no nome do arquivo
        (?=-)                           # seguida de hífen
      |
        matr(?:icula)?\s*               # palavra "matr" ou "matricula"
        [^\d]{0,5}                      # :, *, n°, virgula etc
        (\d{6,10})                      # ← matrícula textual
    )
    """,
    re.IGNORECASE | re.VERBOSE
)
PADRAO_SERIAL = re.compile(
    r"""
    \b(BR[A-Za-z0-9]{8})\b                 # Seriais BRXXXXXXXX
    |
    \bNOTEBOOK\s+([A-Za-z0-9]+)\b          # Após NOTEBOOK
    |
    \bMONITOR\s+([A-Za-z0-9]+)\b           # ✅ Após MONITOR
    |
    \bTR_([A-Za-z0-9]+)-[^\s]+\b           # Dentro de TR_
    """,
    re.IGNORECASE | re.VERBOSE
)

PADRAO_SERIAL_TR = re.compile( r'\bTR_([A-Za-z0-9]{7,})-')
PADRAO_EMAIL= re.compile(r"([a-zA-Z0-9._%+-]+)@")
PADRAO_NOME_ARQUIVO = re.compile(r'(TD|TR)_[^-\s]+-\d+-[^-\s]+', re.IGNORECASE)

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    try:
        with fitz.open(caminho_pdf) as doc:
            for pagina in doc:
                texto += pagina.get_text("text")
    except Exception:
        texto = ""
    return texto.strip()

def extrair_ocr_pdf(caminho_pdf):
    texto_total = ""
    with fitz.open(caminho_pdf) as pdf:
        for pagina in pdf:
            # Renderiza a página como imagem (alta resolução)
            pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_bytes = pix.tobytes("png")
            
            # Converte bytes -> imagem PIL
            imagem = Image.open(io.BytesIO(img_bytes))
            
            # Extrai texto via OCR
            texto_total += pytesseract.image_to_string(imagem) + "\n"
    
    return texto_total.strip()

def processar_pdf(caminho_pdf):
    texto = extrair_texto_pdf(caminho_pdf)
    if not texto:
        print(f"📸 OCR necessário: {os.path.basename(caminho_pdf)}")
        texto = extrair_ocr_pdf(caminho_pdf)
    try:
        texto = texto.replace("\n", " ").replace("\r", " ").replace("  ", " ")
        busca_nome_arquivo = re.search(PADRAO_NOME_ARQUIVO, texto)
        possivel_titulo_completo = busca_nome_arquivo.group(0) if busca_nome_arquivo else None
        # --- Regras de extração ---

        # 1️⃣ Matrícula -> "Matr. " seguido de 6 dígitos
        match_matricula = re.search(PADRAO_MATRICULA, texto)
        matricula = match_matricula.group(1) or match_matricula.group(2) if match_matricula else None

        # 2️⃣ Serial da máquina -> Começa com BR e tem 10 caracteres
        match_serial = re.search(PADRAO_SERIAL, texto)
        serial_maquina = next(g for g in match_serial.groups() if g) if match_serial else None

        # 3️⃣ Usuário portador -> parte antes do @
        match_email = re.search(PADRAO_EMAIL, texto)
        usuario_portador = match_email.group(1) if match_email else None

        # 4️⃣ Tipo de documento
        texto_lower = texto.lower()
        if "responsabilidade" in texto_lower:
            tipo_documento = "TR"
            match_serial_tr = re.search(PADRAO_SERIAL_TR, texto)
            if match_serial_tr:
                serial_maquina = match_serial_tr.group(1)
        elif "devolu" in texto_lower:
            tipo_documento = "TD"
        else:
            tipo_documento = None
            possivel_titulo_completo = None
        if possivel_titulo_completo is None and (matricula is None or serial_maquina is None or usuario_portador is None or tipo_documento is None):
            print(f"texto: {texto}")
            raise ValueError(f"Informações insuficientes para renomear o arquivo. \ntipo_documento: {tipo_documento}\nMatrícula: {matricula}\nSerial: {serial_maquina}\nUsuário: {usuario_portador} \nArquivo: {possivel_titulo_completo}")

        if possivel_titulo_completo:
            novo_nome = possivel_titulo_completo.replace("\n\nPRP", "")
        else:
            novo_nome = f"{tipo_documento}_{serial_maquina}-{matricula}-{usuario_portador}"
        # --- Gera o novo nome ---
        novo_caminho = os.path.join(PASTA, f"{novo_nome}.pdf")
        os.rename(caminho_pdf, novo_caminho)
        print(f"✅ {os.path.basename(caminho_pdf)} → {novo_nome}.pdf")
    except Exception as e:
        print(f"⚠️ Erro ao renomear {os.path.basename(caminho_pdf)}: {e}")

def main():
    for arquivo in os.listdir(PASTA):
        if arquivo.lower().endswith(".pdf"):
            processar_pdf(os.path.join(PASTA, arquivo))

if __name__ == "__main__":
    main()
