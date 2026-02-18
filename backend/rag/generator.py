"""
Generator for RAG pipeline
Generates answers using local Mistral model via Ollama
"""
from typing import List, Dict, Any
from backend.llm.ollama_client import get_ollama_client
from backend.config import SUPPORTED_LANGUAGES


class Generator:
    """Generates answers using local LLM"""
    
    def __init__(self):
        self.ollama_client = get_ollama_client()
    
    def generate_answer(
        self,
        query: str,
        context: str,
        language: str = "en",
        retrieved_docs: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate answer using context and local Mistral model
        
        Args:
            query: User question
            context: Retrieved context from documents
            language: Target language for response
            retrieved_docs: Original retrieved documents
            
        Returns:
            Dictionary with answer, sources, and confidence score
        """
        try:
            # Build prompt with multilingual support
            prompt = self._build_prompt(query, context, language)
            
            # Generate response using Ollama
            response = self.ollama_client.generate(prompt)
            
            # Extract answer and calculate confidence
            answer = response.strip()
            confidence_score = self._calculate_confidence(
                answer, 
                context, 
                retrieved_docs
            )
            
            # Format sources
            sources = self._format_sources(retrieved_docs or [])
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence_score": confidence_score,
                "language": language
            }
            
        except Exception as e:
            raise RuntimeError(f"Answer generation failed: {str(e)}")
    
    def _build_prompt(self, query: str, context: str, language: str) -> str:
        """
        Build prompt for Mistral model with multilingual support
        
        Args:
            query: User question
            context: Retrieved context
            language: Target language
            
        Returns:
            Formatted prompt
        """
        # Get language name
        language_name = SUPPORTED_LANGUAGES.get(language, "English")
        
        # Multilingual instruction
        lang_instruction = ""
        if language != "en":
            lang_instruction = f"\n\nIMPORTANT: Respond ONLY in {language_name}. Translate your entire response to {language_name}."
        
        prompt = f"""You are an expert academic AI assistant for a smart campus knowledge system. 
Your role is to provide accurate, well-structured answers based on the provided context.

CONTEXT FROM DOCUMENTS:
{context}

USER QUESTION:
{query}

INSTRUCTIONS:
1. Answer the question using ONLY the information from the provided context
2. If the context doesn't contain enough information, clearly state that
3. Structure your answer clearly with proper formatting
4. Cite sources by mentioning the document names
5. Be concise but comprehensive
6. Use academic language appropriate for college students and faculty{lang_instruction}

ANSWER:"""
        
        return prompt
    
    def _calculate_confidence(
        self,
        answer: str,
        context: str,
        retrieved_docs: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate confidence score for the answer
        
        Args:
            answer: Generated answer
            context: Retrieved context
            retrieved_docs: Retrieved documents
            
        Returns:
            Confidence score between 0 and 1
        """
        # Base confidence calculation on:
        # 1. Number of retrieved documents
        # 2. Average relevance score
        # 3. Answer length (not too short, not too long)
        # 4. Presence of uncertainty phrases
        
        confidence = 0.5  # Base confidence
        
        # Factor 1: Number of sources
        if retrieved_docs:
            num_sources = len(retrieved_docs)
            if num_sources >= 3:
                confidence += 0.15
            elif num_sources >= 2:
                confidence += 0.10
            elif num_sources >= 1:
                confidence += 0.05
            
            # Factor 2: Average relevance
            avg_relevance = sum(
                doc.get("relevance_score", 0) for doc in retrieved_docs
            ) / len(retrieved_docs)
            confidence += avg_relevance * 0.2
        
        # Factor 3: Answer quality indicators
        answer_lower = answer.lower()
        
        # Decrease confidence for uncertainty phrases
        uncertainty_phrases = [
            "i don't know",
            "not enough information",
            "cannot answer",
            "unclear",
            "insufficient data"
        ]
        
        if any(phrase in answer_lower for phrase in uncertainty_phrases):
            confidence -= 0.2
        
        # Increase confidence if answer mentions sources
        if "source" in answer_lower or "document" in answer_lower:
            confidence += 0.05
        
        # Factor 4: Answer length (reasonable length indicates thoughtful response)
        answer_length = len(answer.split())
        if 50 <= answer_length <= 500:
            confidence += 0.1
        elif answer_length < 20:
            confidence -= 0.1
        
        # Ensure confidence is between 0 and 1
        return max(0.0, min(1.0, confidence))
    
    def _format_sources(self, retrieved_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format source documents for response
        
        Args:
            retrieved_docs: Retrieved documents
            
        Returns:
            List of formatted source dictionaries
        """
        sources = []
        
        for doc in retrieved_docs:
            metadata = doc.get("metadata", {})
            sources.append({
                "filename": metadata.get("filename", "Unknown"),
                "page": metadata.get("page"),
                "chunk_text": doc.get("text", "")[:200] + "...",  # Preview
                "relevance_score": doc.get("relevance_score", 0.0)
            })
        
        return sources


def get_generator() -> Generator:
    """Get generator instance"""
    return Generator()
