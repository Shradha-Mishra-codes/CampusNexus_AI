"""
ChromaDB client for persistent local vector storage
No external APIs - fully local
"""
from typing import List, Dict, Optional, Any
import chromadb
from backend.config import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME, CHROMA_DISTANCE_METRIC


class ChromaDBClient:
    """Client for ChromaDB vector database"""
    
    def __init__(self):
        self.db_path = str(CHROMA_DB_DIR)
        self.collection_name = CHROMA_COLLECTION_NAME
        self.distance_metric = CHROMA_DISTANCE_METRIC
        self.client: Optional[chromadb.Client] = None
        self.collection = None
        self._initialize()
    
    def _initialize(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create persistent client
            self.client = chromadb.PersistentClient(
                path=self.db_path
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": self.distance_metric}
            )
            
            print(f"✓ ChromaDB initialized at {self.db_path}")
            print(f"✓ Collection '{self.collection_name}' ready")
            
        except Exception as e:
            print(f"✗ Failed to initialize ChromaDB: {str(e)}")
            raise
    
    def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ):
        """
        Add documents to the collection
        
        Args:
            texts: List of text chunks
            embeddings: List of embedding vectors
            metadatas: List of metadata dicts
            ids: List of unique IDs for documents
        """
        try:
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✓ Added {len(texts)} documents to ChromaDB")
        except Exception as e:
            raise RuntimeError(f"Failed to add documents: {str(e)}")
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            Dictionary with ids, documents, metadatas, and distances
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_dict
            )
            return results
        except Exception as e:
            raise RuntimeError(f"Search failed: {str(e)}")
    
    def get_document_count(self) -> int:
        """Get total number of documents in collection"""
        try:
            return self.collection.count()
        except Exception as e:
            print(f"Error getting document count: {str(e)}")
            return 0
    
    def delete_documents(self, ids: List[str]):
        """Delete documents by IDs"""
        try:
            self.collection.delete(ids=ids)
            print(f"✓ Deleted {len(ids)} documents")
        except Exception as e:
            raise RuntimeError(f"Failed to delete documents: {str(e)}")
    
    def reset_collection(self):
        """Reset the entire collection (use with caution!)"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": self.distance_metric}
            )
            print("✓ Collection reset")
        except Exception as e:
            raise RuntimeError(f"Failed to reset collection: {str(e)}")
    
    def get_all_documents_metadata(self) -> List[Dict[str, Any]]:
        """Get metadata for all documents"""
        try:
            results = self.collection.get()
            metadatas = results.get("metadatas", [])
            return metadatas
        except Exception as e:
            print(f"Error getting all documents: {str(e)}")
            return []
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents with their text content and metadata"""
        try:
            results = self.collection.get()
            documents = results.get("documents", [])
            metadatas = results.get("metadatas", [])
            ids = results.get("ids", [])
            
            # Combine text, metadata, and id into a single dict
            docs = []
            for i in range(len(documents)):
                doc = {
                    "id": ids[i] if i < len(ids) else "",
                    "text": documents[i] if i < len(documents) else "",
                    "metadata": metadatas[i] if i < len(metadatas) else {}
                }
                docs.append(doc)
            
            return docs
        except Exception as e:
            print(f"Error getting all documents: {str(e)}")
            return []
    
    def check_health(self) -> bool:
        """Check if ChromaDB is working properly"""
        try:
            _ = self.collection.count()
            return True
        except Exception:
            return False


# Global instance
_chroma_client: Optional[ChromaDBClient] = None


def get_chroma_client() -> ChromaDBClient:
    """Get or create global ChromaDB client instance"""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = ChromaDBClient()
    return _chroma_client
