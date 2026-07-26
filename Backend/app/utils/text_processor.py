import re
import unicodedata
from typing import List
from pypdf import PdfReader
from io import BytesIO

def normalize_bangla_text(text: str) -> str:
    """Performs NFC Unicode normalization for Bangla scripts."""
    if not text:
        return ""
    normalized = unicodedata.normalize('NFC', text)
    return re.sub(r'\s+', ' ', normalized).strip()

def parse_file_content(filename: str, content_bytes: bytes) -> str:
    """Parses text content from PDF, TXT, or MD bytes."""
    ext = filename.split('.')[-1].lower()
    if ext == 'pdf':
        reader = PdfReader(BytesIO(content_bytes))
        extracted_text = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                extracted_text.append(t)
        return "\n".join(extracted_text)
    else:
        # TXT, MD or generic UTF-8 text
        return content_bytes.decode('utf-8', errors='ignore')

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    """Splits text into overlapping chunks respecting sentence boundaries."""
    normalized_text = normalize_bangla_text(text)
    sentences = re.split(r'(?<=[।!?\n])', normalized_text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        words = sentence.split()
        if current_length + len(words) > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            # Keep overlap words
            overlap_words = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
            current_chunk = list(overlap_words)
            current_length = len(current_chunk)
            
        current_chunk.extend(words)
        current_length += len(words)
        
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
