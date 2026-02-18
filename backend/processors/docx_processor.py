"""
DOCX document processor
Extracts text from Word documents
"""
from typing import Dict, Any
from pathlib import Path
from docx import Document
from backend.processors.text_chunker import get_text_chunker


class DOCXProcessor:
    """Processes DOCX documents"""
    
    def __init__(self):
        self.chunker = get_text_chunker()
    
    def process(self, file_path: Path) -> Dict[str, Any]:
        """
        Process DOCX file
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Dictionary with chunks and metadata
        """
        try:
            doc = Document(file_path)
            
            # Extract all paragraphs
            all_text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    all_text.append(paragraph.text)
            
            # Combine into single text
            full_text = "\n\n".join(all_text)
            
            # Chunk the text
            chunks = self.chunker.chunk_text(full_text)
            
            # Create metadata for each chunk
            chunk_metadatas = []
            for _ in chunks:
                chunk_metadatas.append({
                    "filename": file_path.name,
                    "file_type": "docx",
                    "page": None  # DOCX doesn't have page numbers
                })
            
            return {
                "chunks": chunks,
                "metadatas": chunk_metadatas,
                "total_pages": None,
                "total_chunks": len(chunks)
            }
            
        except Exception as e:
            raise RuntimeError(f"DOCX processing failed: {str(e)}")


def get_docx_processor() -> DOCXProcessor:
    """Get DOCXProcessor instance"""
    return DOCXProcessor()
