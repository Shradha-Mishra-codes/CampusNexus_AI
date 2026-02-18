"""
PDF document processor
Extracts text and metadata from PDF files
"""
from typing import List, Dict, Any
from pathlib import Path
import pypdf
from backend.processors.text_chunker import get_text_chunker


class PDFProcessor:
    """Processes PDF documents"""
    
    def __init__(self):
        self.chunker = get_text_chunker()
    
    def process(self, file_path: Path) -> Dict[str, Any]:
        """
        Process PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary with chunks and metadata
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                total_pages = len(pdf_reader.pages)
                all_chunks = []
                chunk_metadatas = []
                
                # Extract text from each page
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    
                    if page_text.strip():
                        # Chunk the page text
                        chunks = self.chunker.chunk_text(page_text)
                        
                        # Create metadata for each chunk
                        for chunk in chunks:
                            all_chunks.append(chunk)
                            chunk_metadatas.append({
                                "filename": file_path.name,
                                "file_type": "pdf",
                                "page": page_num,
                                "total_pages": total_pages
                            })
                
                return {
                    "chunks": all_chunks,
                    "metadatas": chunk_metadatas,
                    "total_pages": total_pages,
                    "total_chunks": len(all_chunks)
                }
                
        except Exception as e:
            raise RuntimeError(f"PDF processing failed: {str(e)}")


def get_pdf_processor() -> PDFProcessor:
    """Get PDFProcessor instance"""
    return PDFProcessor()
