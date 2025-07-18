import os
import fitz
import docx
from bs4 import BeautifulSoup
from app.vector_store import add_to_vector_store


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)


def extract_text_from_docx(path):
    return "\n".join(p.text for p in docx.Document(path).paragraphs)


def extract_text_from_email(path):
    with open(path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        return soup.get_text()


def parse_and_index_file(path):
    if path.endswith(".pdf"):
        text = extract_text_from_pdf(path)
    elif path.endswith(".docx"):
        text = extract_text_from_docx(path)
    elif path.endswith(".eml"):
        text = extract_text_from_email(path)
    else:
        raise ValueError("Unsupported format")

    add_to_vector_store(text, os.path.basename(path))
