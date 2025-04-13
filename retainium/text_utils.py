# Module for various text processing utilities

# Import required modules
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from typing import List
import re
from retainium.diagnostics import Diagnostics

# Remove excessive whitespace and line breaks
def clean_text(text: str) -> str:
    # Eliminate noisy lines
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.fullmatch(r'\d{1,3}', stripped):
            continue
        if re.fullmatch(r'[A-Za-z0-9]{1,3}', stripped):
            continue
        cleaned_lines.append(stripped)
    
    # Cleanup remaining text
    text = "\n".join(cleaned_lines)
    text = re.sub(r'\n\s*\n+', '\n\n', text)  # collapse multiple empty lines
    text = re.sub(r'[ \t]+', ' ', text)       # normalize spaces and tabs
    text = re.sub(r' +\n', '\n', text)        # remove trailing spaces at line ends
    return text.strip()

# Chunk text using LangChain's RecursiveCharacterTextSplitter
def chunk_text(text: str, chunk_size: int = 300, chunk_overlap: int = 50) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    return splitter.split_text(text)

# Heuristic to detect if text is mostly unusable 
# (e.g., vertical letters, too much whitespace, etc.)
def looks_like_garbage(text: str) -> bool:
    lines = text.splitlines()
    if not lines:
        return True

    # Heuristics - lines with single characters, avg length of lines in text
    total_line_len = max(len(lines), 1)
    single_char_lines = sum(1 for line in lines if len(line.strip()) <= 2)
    short_lines = sum(1 for line in lines if len(line.strip()) < 20)
    avg_line_length = sum(len(line.strip()) for line in lines) / total_line_len

    return (
            (short_lines / total_line_len) > 0.6 
            or
            (avg_line_length < 10 and single_char_lines > 0.5 * len(lines))
           )

# Extract text using OCR from scanned/image-only PDFs
def extract_text_via_ocr(pdf_path: str) -> str:
    images = convert_from_path(pdf_path, dpi=300)
    ocr_text = []

    for idx, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        ocr_text.append(f"[Page {idx + 1}]\n{text.strip()}")

    return "\n\n".join(ocr_text)

# Extract text using PyMuPDF 
# (if empty or garbage, fallback to OCR)
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    all_text = [page.get_text() for page in doc]
    full_text = "\n".join(all_text).strip()

    # Check for extraction quality and fallback on OCR if required
    if not full_text or looks_like_garbage(full_text):
        Diagnostics.warning("falling back to OCR due to poor fitz extraction")
        full_text = extract_text_via_ocr(pdf_path)

    return clean_text(full_text)

# Extract and chunk text from a PDF file with OCR fallback and quality check
def extract_and_chunk_pdf(pdf_path: str, chunk_size: int = 300, chunk_overlap: int = 50) -> List[str]:
    raw_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(raw_text, chunk_size, chunk_overlap)
    ''' Example
        Diagnostics.note(f"Total {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            Diagnostics.note(f"--- Chunk {i+1} ---")
            print(f"{chunk}")
    '''
    return chunks

