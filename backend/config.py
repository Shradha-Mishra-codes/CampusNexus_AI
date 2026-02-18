"""
Configuration settings for CampusNexus AI
All settings for local, offline operation
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DB_DIR = DATA_DIR / "chroma_db"
UPLOADS_DIR = BASE_DIR / "uploads"

# Create directories if they don't exist
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"
OLLAMA_TIMEOUT = 120  # seconds

# Embedding Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DEVICE = "cpu"  # Use "cuda" if GPU available

# ChromaDB Configuration
CHROMA_COLLECTION_NAME = "campus_documents"
CHROMA_DISTANCE_METRIC = "cosine"

# RAG Configuration
TOP_K_RETRIEVAL = 5
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_CONTEXT_LENGTH = 4000

# Supported file types
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".txt"}

# Multilingual Support
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German"
}

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
CORS_ORIGINS = ["*"]

# Feature Flags
ENABLE_PYQ_ANALYTICS = True
ENABLE_KNOWLEDGE_GRAPH = True
ENABLE_MULTILINGUAL = True
ENABLE_GOVERNANCE = True
