import os
import fitz
import docx
from bs4 import BeautifulSoup


def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = " ".join(page.get_text() for page in doc)
    doc.close()
    return text


def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text_from_email(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


def save_and_extract(file):
    filename = file.filename
    filepath = os.path.join("uploads", filename)
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    ext = filename.lower().split('.')[-1]
    if ext == "pdf":
        return extract_text_from_pdf(filepath)
    elif ext == "docx":
        return extract_text_from_docx(filepath)
    elif ext in ["eml", "html"]:
        return extract_text_from_email(filepath)
    else:
        raise ValueError("Unsupported file type")
