from fastapi import UploadFile
import pdfplumber

async def extract_text_from_file(file: UploadFile) -> str:
    if file.filename.endswith(".txt"):
        content = await file.read()
        return content.decode("utf-8")

    if file.filename.endswith(".pdf"):
        file.file.seek(0)
        text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    raise ValueError("Formato de arquivo não suportado")
