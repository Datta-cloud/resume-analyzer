# resume_parser.py
import fitz  # pymupdf
from docx import Document


def read_pdf(file) -> str:
    """Read PDF using PyMuPDF (no DLL issues on Windows)"""
    pdf_bytes = file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    return text.strip()


def read_docx(file) -> str:
    """Read DOCX Word file"""
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()


def parse_resume(uploaded_file) -> str:
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        return read_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return read_docx(uploaded_file)
    else:
        return ""