"""
Local embeddings using SentenceTransformers
No API calls - fully offline
"""
from typing import List, Union
from sentence_transformers import SentenceTransformer
from backend.config import EMBEDDING_MODEL, EMBEDDING_DEVICE


class LocalEmbeddings:
    """Local embedding model using SentenceTransformers"""
    
    def __init__(self):
        self.model_name = EMBEDDING_MODEL
        self.device = EMBEDDING_DEVICE
        self.model: SentenceTransformer = None
        self._initialize()
    
    def _initialize(self):
        """Load the embedding model"""
        try:
            print(f"Loading embedding model: {self.model_name}...")
            self.model = SentenceTransformer(
                self.model_name,
                device=self.device
            )
            print(f"✓ Embedding model loaded on {self.device}")
        except Exception as e:
            print(f"✗ Failed to load embedding model: {str(e)}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """
        Embed a single text string
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list of floats
        """
        if not self.model:
            raise RuntimeError("Embedding model not initialized")
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Embed multiple texts in batch
        
        Args:
            texts: List of input texts
            batch_size: Batch size for encoding
            
        Returns:
            List of embedding vectors
        """
        if not self.model:
            raise RuntimeError("Embedding model not initialized")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > 100
        )
        return [emb.tolist() for emb in embeddings]
    
    def embed_query(self, query: str) -> List[float]:
        """
        Embed a query string
        Same as embed_text but provided for API consistency
        
        Args:
            query: Query text
            
        Returns:
            Embedding vector
        """
        return self.embed_text(query)
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        if not self.model:
            raise RuntimeError("Embedding model not initialized")
        return self.model.get_sentence_embedding_dimension()


# Global instance
_embedding_model: Union[LocalEmbeddings, None] = None


def get_embedding_model() -> LocalEmbeddings:
    """Get or create global embedding model instance"""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = LocalEmbeddings()
    return _embedding_model
