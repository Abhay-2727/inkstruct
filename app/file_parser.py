"""file_parser.py — extract plain text from uploaded .txt, .docx, .pdf files."""

from docx import Document
from pypdf import PdfReader


def extract_text_from_txt(file) -> str:
    """Extract text from an uploaded .txt file."""
    raw_bytes = file.read()
    return raw_bytes.decode("utf-8", errors="replace")


def extract_text_from_docx(file) -> str:
    """Extract text from an uploaded .docx file."""
    document = Document(file)
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)


def extract_text_from_pdf(file) -> str:
    """Extract text from an uploaded .pdf file."""
    reader = PdfReader(file)
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)
    return "\n".join(pages_text)


def extract_text(file) -> str:
    """Route an uploaded file to the correct extractor based on its extension."""
    filename = file.name.lower()

    if filename.endswith(".txt"):
        return extract_text_from_txt(file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)
    elif filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    else:
        raise ValueError(f"Unsupported file type: {filename}")