"""
Ollama LLM client for local inference
No API keys required - fully local
"""
import requests
from typing import Optional
from langchain_community.llms import Ollama
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT


class OllamaClient:
    """Client for interacting with local Ollama instance"""
    
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model = OLLAMA_MODEL
        self.timeout = OLLAMA_TIMEOUT
        self.llm: Optional[Ollama] = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Ollama LLM"""
        try:
            # Check if Ollama is running
            if not self.check_health():
                raise ConnectionError(
                    "Ollama is not running. Please start Ollama and ensure "
                    f"the '{self.model}' model is available.\n\n"
                    f"Install Ollama: https://ollama.ai\n"
                    f"Then run: ollama pull {self.model}"
                )
            
            # Initialize LangChain Ollama
            self.llm = Ollama(
                base_url=self.base_url,
                model=self.model,
                timeout=self.timeout
            )
            print(f"✓ Ollama client initialized with model: {self.model}")
            
        except Exception as e:
            print(f"✗ Failed to initialize Ollama: {str(e)}")
            raise
    
    def check_health(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            # Check if Ollama API is accessible
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            
            if response.status_code != 200:
                return False
            
            # Check if our model is available
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            
            # Check for exact match or partial match (e.g., "mistral:latest")
            model_available = any(
                self.model in name for name in model_names
            )
            
            if not model_available:
                print(f"Model '{self.model}' not found. Available models: {model_names}")
                print(f"Please run: ollama pull {self.model}")
                return False
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Cannot connect to Ollama at {self.base_url}")
            print(f"Error: {str(e)}")
            return False
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Ollama
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters for generation
            
        Returns:
            Generated text
        """
        if not self.llm:
            raise RuntimeError("Ollama client not initialized")
        
        try:
            response = self.llm.invoke(prompt, **kwargs)
            return response
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {str(e)}")
    
    def get_status(self) -> dict:
        """Get current status of Ollama connection"""
        return {
            "connected": self.check_health(),
            "base_url": self.base_url,
            "model": self.model,
            "initialized": self.llm is not None
        }


# Global instance
_ollama_client: Optional[OllamaClient] = None


def get_ollama_client() -> OllamaClient:
    """Get or create global Ollama client instance"""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client
