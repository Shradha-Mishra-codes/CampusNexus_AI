"""
Retriever for RAG pipeline
Handles semantic search and context retrieval from ChromaDB
"""
from typing import List, Dict, Any, Optional
from backend.vector_store.chroma_client import get_chroma_client
from backend.llm.embeddings import get_embedding_model
from backend.config import TOP_K_RETRIEVAL


class Retriever:
    """Retrieves relevant documents from vector store"""
    
    def __init__(self):
        self.chroma_client = get_chroma_client()
        self.embedding_model = get_embedding_model()
    
    def retrieve(
        self,
        query: str,
        top_k: int = TOP_K_RETRIEVAL,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
            filter_metadata: Optional metadata filters
            
        Returns:
            List of retrieved documents with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.embed_query(query)
            
            # Search in ChromaDB
            results = self.chroma_client.search(
                query_embedding=query_embedding,
                top_k=top_k,
                filter_dict=filter_metadata
            )
            
            # Format results
            retrieved_docs = []
            
            if results and "documents" in results:
                docs = results["documents"][0] if results["documents"] else []
                metadatas = results["metadatas"][0] if results["metadatas"] else []
                distances = results["distances"][0] if results["distances"] else []
                
                for i, doc in enumerate(docs):
                    metadata = metadatas[i] if i < len(metadatas) else {}
                    distance = distances[i] if i < len(distances) else 1.0
                    
                    # Convert distance to similarity score (0-1)
                    # For cosine distance: similarity = 1 - distance
                    similarity = max(0.0, 1.0 - distance)
                    
                    retrieved_docs.append({
                        "text": doc,
                        "metadata": metadata,
                        "relevance_score": similarity
                    })
            
            return retrieved_docs
            
        except Exception as e:
            raise RuntimeError(f"Retrieval failed: {str(e)}")
    
    def build_context(self, retrieved_docs: List[Dict[str, Any]], max_length: int = 4000) -> str:
        """
        Build context string from retrieved documents
        
        Args:
            retrieved_docs: List of retrieved documents
            max_length: Maximum context length in characters
            
        Returns:
            Formatted context string
        """
        context_parts = []
        current_length = 0
        
        for i, doc in enumerate(retrieved_docs, 1):
            text = doc["text"]
            metadata = doc["metadata"]
            
            # Format with source information
            source = metadata.get("filename", "Unknown")
            page = metadata.get("page", "")
            page_info = f" (Page {page})" if page else ""
            
            doc_text = f"[Source {i}: {source}{page_info}]\n{text}\n\n"
            
            # Check if adding this would exceed max length
            if current_length + len(doc_text) > max_length:
                break
            
            context_parts.append(doc_text)
            current_length += len(doc_text)
        
        return "".join(context_parts)


def get_retriever() -> Retriever:
    """Get retriever instance"""
    return Retriever()
