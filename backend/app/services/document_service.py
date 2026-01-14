"""
Document Service - PDF processing and text chunking
Handles document upload, text extraction, and chunking for RAG
"""

import logging
import os
import re
import uuid
from pathlib import Path
from typing import Optional, List, Tuple

from app.config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Service for processing documents (PDF extraction and chunking)"""
    
    def __init__(
        self, 
        chunk_size: Optional[int] = None, 
        chunk_overlap: Optional[int] = None
    ):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        self.documents_dir = Path("data/documents")
        self.documents_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Document Processor initialized (chunk_size={self.chunk_size}, overlap={self.chunk_overlap})")
    
    def save_uploaded_file(self, file_content: bytes, filename: str) -> str:
        """
        Save uploaded file to disk.
        
        Args:
            file_content: Binary content of the file
            filename: Original filename
            
        Returns:
            Path to saved file
        """
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        safe_filename = self._sanitize_filename(filename)
        file_path = self.documents_dir / f"{unique_id}_{safe_filename}"
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        logger.info(f"File saved: {file_path}")
        return str(file_path)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Remove unsafe characters from filename"""
        # Keep only alphanumeric, dots, underscores, hyphens
        safe = re.sub(r'[^\w\-.]', '_', filename)
        return safe
    
    def extract_text_from_pdf(self, file_path: str) -> Tuple[str, int]:
        """
        Extract text content from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, page_count)
        """
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(file_path)
            page_count = len(reader.pages)
            
            text_parts = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"[PAGE {i+1}]\n{page_text}")
            
            full_text = "\n\n".join(text_parts)
            logger.info(f"Extracted text from {page_count} pages")
            return full_text, page_count
            
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            raise
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special control characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Fix common OCR issues
        text = text.replace('ﬁ', 'fi')
        text = text.replace('ﬂ', 'fl')
        
        return text.strip()
    
    def chunk_text(
        self, 
        text: str, 
        chunk_size: Optional[int] = None,
        overlap: Optional[int] = None
    ) -> List[dict]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to split
            chunk_size: Target chunk size in words
            overlap: Number of overlapping words between chunks
            
        Returns:
            List of chunk dictionaries with content and metadata
        """
        chunk_size = chunk_size or self.chunk_size
        overlap = overlap or self.chunk_overlap
        
        # Split by words while preserving page markers
        words = text.split()
        chunks = []
        chunk_index = 0
        
        i = 0
        current_page = 1
        
        while i < len(words):
            # Get chunk words
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            # Only add if chunk is substantial
            if len(chunk_text) > 50:
                # Detect page number from content
                page_match = re.search(r'\[PAGE (\d+)\]', chunk_text)
                if page_match:
                    current_page = int(page_match.group(1))
                
                # Clean page markers from chunk
                clean_chunk = re.sub(r'\[PAGE \d+\]', '', chunk_text).strip()
                
                chunks.append({
                    'chunk_index': chunk_index,
                    'content': clean_chunk,
                    'page_number': current_page,
                    'word_count': len(chunk_words)
                })
                chunk_index += 1
            
            # Move forward with overlap
            i += chunk_size - overlap
        
        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks
    
    def process_document(
        self, 
        file_path: str, 
        title: Optional[str] = None
    ) -> dict:
        """
        Process a document end-to-end: extract, clean, and chunk.
        
        Args:
            file_path: Path to the document
            title: Optional document title
            
        Returns:
            Dictionary with document info and chunks
        """
        # Extract text
        raw_text, page_count = self.extract_text_from_pdf(file_path)
        
        # Clean text
        clean_text = self.clean_text(raw_text)
        
        # Create chunks
        chunks = self.chunk_text(raw_text)  # Use raw to preserve page markers
        
        # Clean each chunk
        for chunk in chunks:
            chunk['content'] = self.clean_text(chunk['content'])
        
        return {
            'file_path': file_path,
            'title': title or Path(file_path).stem,
            'content': clean_text,
            'page_count': page_count,
            'chunks': chunks,
            'total_chunks': len(chunks)
        }


# Singleton instance
_document_processor: Optional[DocumentProcessor] = None


def get_document_processor() -> DocumentProcessor:
    """Get or create document processor singleton"""
    global _document_processor
    if _document_processor is None:
        _document_processor = DocumentProcessor()
    return _document_processor
