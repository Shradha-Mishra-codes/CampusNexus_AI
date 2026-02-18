from backend.vector_store.chroma_client import get_chroma_client
try:
    print("Attempting to initialize ChromaDBClient...")
    client = get_chroma_client()
    print("Success!")
    # Test reset collection if needed, but for now just init is enough
except Exception as e:
    print(f"Failed: {e}")
