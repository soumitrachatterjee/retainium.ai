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

# Singleton class, enabling easy global access to all configured values
class TextHandler:
    _instance = None

    def __new__(cls, config=None):
        if cls._instance is None:
            cls._instance = super(TextHandler, cls).__new__(cls)
            cls._instance._initialize(config)
        return cls._instance

    # Initialize with values from configuration file; fallback on defaults
    def _initialize(self, config):
        # Chunking configuration
        self.chunking_enabled = config.getboolean("chunking", "enabled", fallback=True)
        self.chunk_size = config.getint("chunking", "chunk_size", fallback=512)
        self.chunk_overlap = config.getint("chunking", "chunk_overlap", fallback=64)
        self.chunk_size_fallback = config.getint("chunking", 
                                                 "chunk_size_fallback", 
                                                 fallback=256)
        self.single_char_line_threshold = config.getfloat("chunking", 
                                                          "single_char_line_threshold", 
                                                          fallback=0.5)
        self.short_line_threshold = config.getfloat("chunking", 
                                                    "short_line_threshold", 
                                                    fallback=0.6)
        self.avg_line_length_threshold = config.getfloat("chunking", 
                                                         "avg_line_length_threshold",
                                                         fallback=10)
        # OCR configuration
        self.ocr_enabled = config.getboolean("ocr", "enabled", fallback=True)
        self.ocr_dpi = config.getint("ocr", "dpi", fallback=300)
        Diagnostics.note(f"text handler initialized with chunk_size={self.chunk_size}")

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
def chunk_text(text: str) -> List[str]:
    text_handler = TextHandler()
    if text_handler.chunking_enabled:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=text_handler.chunk_size,
            chunk_overlap=text_handler.chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )
        return splitter.split_text(text)
    else:
        Diagnostics.warning(f"text chunking disabled")
        return [text.strip()]

# Heuristic to detect if text is mostly unusable 
# (e.g., vertical letters, too much whitespace, etc.)
def looks_like_garbage(text: str) -> bool:
    text_handler = TextHandler()
    lines = text.splitlines()
    if not lines:
        return True

    # Heuristics - lines with single characters, avg length of lines in text
    total_line_len = max(len(lines), 1)
    single_char_lines = sum(1 for line in lines if len(line.strip()) <= 2)
    short_lines = sum(1 for line in lines if len(line.strip()) < 20)
    avg_line_length = sum(len(line.strip()) for line in lines) / total_line_len

    single_char_lines_ratio = single_char_lines / total_line_len
    short_line_ratio = short_lines / total_line_len
    Diagnostics.debug(f"Single line ratio: {single_char_lines_ratio}")
    Diagnostics.debug(f"Short line ratio: {short_line_ratio}")
    Diagnostics.debug(f"Average line length: {avg_line_length}")
    return (
            short_line_ratio > text_handler.single_char_line_threshold 
            or
            (
                avg_line_length < text_handler.avg_line_length_threshold 
                and 
                single_char_lines_ratio > text_handler.single_char_line_threshold
            )
           )

# Extract text using OCR from scanned/image-only PDFs
def extract_text_via_ocr(pdf_path: str) -> str:
    text_handler = TextHandler()
    if text_handler.ocr_enabled:
        images = convert_from_path(pdf_path, text_handler.ocr_dpi)
        ocr_text = []

        for idx, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            ocr_text.append(f"[Page {idx + 1}]\n{text.strip()}")

        return "\n\n".join(ocr_text)
    else:
        Diagnostics.warning(f"OCR disabled")
        return ""

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
def extract_and_chunk_pdf(pdf_path: str) -> List[str]:
    raw_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(raw_text)
    ''' Example
        Diagnostics.note(f"Total {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            Diagnostics.note(f"--- Chunk {i+1} ---")
            print(f"{chunk}")
    '''
    return chunks

