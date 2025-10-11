import os
import re
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
from tkinter import filedialog, Tk

def escolher_pasta():
    root = Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title="Selecione a pasta com PDFs")
    return pasta

# --- Configurações ---
PASTA = escolher_pasta()

# Regex para detectar algo no texto (exemplo: CPF)
PADRAO_MATRICULA = re.compile(r"Matr\.?\s*(\d{6})")
PADRAO_SERIAL = re.compile(r"\b(BR[A-Za-z0-9]{8})\b")
PADRAO_EMAIL= re.compile(r"([a-zA-Z0-9._%+-]+)@")

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
    imagens = convert_from_path(caminho_pdf)
    texto = ""
    for img in imagens:
        texto += pytesseract.image_to_string(img, lang="por")
    return texto.strip()

def processar_pdf(caminho_pdf):
    texto = extrair_texto_pdf(caminho_pdf)
    if not texto:
        print(f"📸 OCR necessário: {os.path.basename(caminho_pdf)}")
        texto = extrair_ocr_pdf(caminho_pdf)
    try:
        # --- Regras de extração ---

        # 1️⃣ Matrícula -> "Matr. " seguido de 6 dígitos
        match_matricula = re.search(PADRAO_MATRICULA, texto)
        matricula = match_matricula.group(1) if match_matricula else None

        # 2️⃣ Serial da máquina -> Começa com BR e tem 10 caracteres
        match_serial = re.search(PADRAO_SERIAL, texto)
        serialMaquina = match_serial.group(1) if match_serial else None

        # 3️⃣ Usuário portador -> parte antes do @
        match_email = re.search(PADRAO_EMAIL, texto)
        usuarioPortador = match_email.group(1) if match_email else None

        # 4️⃣ Tipo de documento
        texto_lower = texto.lower()
        if "termo de responsabilidade" in texto_lower:
            tipoDocumento = "TR"
        elif "termo de devolução" in texto_lower:
            tipoDocumento = "TD"
        else:
            None
        if matricula is None or serialMaquina is None or usuarioPortador is None or tipoDocumento is None:
            raise Exception("Informações insuficientes para renomear o arquivo.")

        # --- Gera o novo nome ---
        novo_nome = f"{tipoDocumento}_{matricula}_{usuarioPortador}_{serialMaquina}".upper()
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
