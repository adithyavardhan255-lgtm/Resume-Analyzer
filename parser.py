"""Module 1: Resume Parser - extracts raw text from PDF, DOCX and TXT files."""
from pypdf import PdfReader
from docx import Document


def extract_text(file_obj, filename: str) -> str:
    """Return plain text from an uploaded resume file."""
    name = filename.lower()
    if name.endswith(".pdf"):
        reader = PdfReader(file_obj)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if name.endswith(".docx"):
        doc = Document(file_obj)
        return "\n".join(p.text for p in doc.paragraphs)
    if name.endswith(".txt"):
        data = file_obj.read()
        return data.decode("utf-8", errors="ignore") if isinstance(data, bytes) else data
    raise ValueError("Unsupported file type. Please upload PDF, DOCX or TXT.")
