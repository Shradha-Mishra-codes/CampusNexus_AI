"""
Smart text chunking for documents
Splits text into manageable chunks with overlap
"""
from typing import List


class TextChunker:
    """Chunks text into smaller pieces for embedding"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize chunker
        
        Args:
            chunk_size: Target size for each chunk (in characters)
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        if not text or len(text) == 0:
            return []
        
        # If text is smaller than chunk size, return as single chunk
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If this is not the last chunk, try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings near the end position
                sentence_endings = ['. ', '.\n', '! ', '!\n', '? ', '?\n']
                best_break = end
                
                # Search window around end position
                search_start = max(start + self.chunk_size - 100, start)
                search_end = min(end + 100, len(text))
                search_text = text[search_start:search_end]
                
                # Find the last sentence ending in the window
                for ending in sentence_endings:
                    last_pos = search_text.rfind(ending)
                    if last_pos != -1:
                        actual_pos = search_start + last_pos + len(ending)
                        if actual_pos > start:
                            best_break = actual_pos
                            break
                
                end = best_break
            
            # Extract chunk
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            
            # Avoid infinite loop
            if start >= len(text):
                break
        
        return chunks


def get_text_chunker(chunk_size: int = 1000, chunk_overlap: int = 200) -> TextChunker:
    """Get a TextChunker instance"""
    return TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
