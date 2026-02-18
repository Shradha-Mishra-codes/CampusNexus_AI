"""
CampusNexus AI - Main FastAPI Application
Fully local, offline AI-powered knowledge search system
No API keys required
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import time
import uuid
from typing import Dict

from backend.config import (
    API_HOST,
    API_PORT,
    CORS_ORIGINS,
    UPLOADS_DIR,
    SUPPORTED_EXTENSIONS
)
from backend.models import (
    ChatQuery,
    ChatResponse,
    UploadResponse,
    DocumentMetadata,
    HealthCheck,
    PYQAnalyticsResponse,
    KnowledgeGraphResponse,
    DocumentApprovalRequest,
    GovernanceStats
)
from backend.llm.ollama_client import get_ollama_client
from backend.llm.embeddings import get_embedding_model
from backend.vector_store.chroma_client import get_chroma_client
from backend.rag.retriever import get_retriever
from backend.rag.generator import get_generator
from backend.processors.pdf_processor import get_pdf_processor
from backend.processors.docx_processor import get_docx_processor
from backend.processors.pptx_processor import get_pptx_processor
from backend.features.pyq_analytics import get_pyq_analytics
from backend.features.knowledge_graph import get_knowledge_graph
from backend.features.governance import get_governance_panel

# Initialize FastAPI app
app = FastAPI(
    title="CampusNexus AI",
    description="Local offline AI-powered knowledge search for smart campuses",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("=" * 60)
    print("🚀 CampusNexus AI Starting...")
    print("=" * 60)
    
    try:
        # Initialize all services
        ollama = get_ollama_client()
        embeddings = get_embedding_model()
        chroma = get_chroma_client()
        
        print("\n✅ All services initialized successfully!")
        print(f"📊 Documents in database: {chroma.get_document_count()}")
        print(f"🌐 Server running at http://{API_HOST}:{API_PORT}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {str(e)}")
        print("\n⚠️  Make sure Ollama is running and Mistral model is available:")
        print("   1. Install Ollama: https://ollama.ai")
        print("   2. Run: ollama pull mistral")
        print("=" * 60)


@app.get("/")
async def root():
    """Serve the frontend"""
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "CampusNexus AI API is running. Frontend not found."}


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    try:
        ollama = get_ollama_client()
        chroma = get_chroma_client()
        
        ollama_status = "connected" if ollama.check_health() else "disconnected"
        chroma_status = "connected" if chroma.check_health() else "disconnected"
        
        overall_status = "healthy" if (ollama_status == "connected" and chroma_status == "connected") else "degraded"
        
        return HealthCheck(
            status=overall_status,
            ollama_status=ollama_status,
            chroma_status=chroma_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Validate file type
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported: {SUPPORTED_EXTENSIONS}"
            )
        
        # Save file
        document_id = str(uuid.uuid4())
        file_path = UPLOADS_DIR / f"{document_id}_{file.filename}"
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process based on file type
        if file_ext == ".pdf":
            processor = get_pdf_processor()
        elif file_ext == ".docx":
            processor = get_docx_processor()
        elif file_ext == ".pptx":
            processor = get_pptx_processor()
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        result = processor.process(file_path)
        chunks = result["chunks"]
        metadatas = result["metadatas"]
        
        # Generate embeddings
        embeddings_model = get_embedding_model()
        embeddings = embeddings_model.embed_batch(chunks)
        
        # Store in ChromaDB
        chroma = get_chroma_client()
        chunk_ids = [f"{document_id}_{i}" for i in range(len(chunks))]
        chroma.add_documents(
            texts=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=chunk_ids
        )
        
        # Register in governance
        governance = get_governance_panel()
        governance.register_document(
            document_id=document_id,
            filename=file.filename,
            file_type=file_ext[1:]  # Remove dot
        )
        
        return UploadResponse(
            success=True,
            message="Document processed and indexed successfully",
            document_id=document_id,
            metadata=DocumentMetadata(
                filename=file.filename,
                file_type=file_ext[1:],
                total_pages=result.get("total_pages"),
                total_chunks=result["total_chunks"]
            )
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(query: ChatQuery):
    """Chat with RAG system"""
    try:
        start_time = time.time()
        
        # Log query
        governance = get_governance_panel()
        governance.log_query(query.query)
        
        # Retrieve relevant documents
        retriever = get_retriever()
        retrieved_docs = retriever.retrieve(
            query=query.query,
            top_k=query.top_k
        )
        
        if not retrieved_docs:
            return ChatResponse(
                answer="I couldn't find any relevant information in the knowledge base. Please upload documents first.",
                sources=[],
                confidence_score=0.0,
                language=query.language,
                processing_time=time.time() - start_time
            )
        
        # Build context
        context = retriever.build_context(retrieved_docs)
        
        # Generate answer
        generator = get_generator()
        result = generator.generate_answer(
            query=query.query,
            context=context,
            language=query.language,
            retrieved_docs=retrieved_docs
        )
        
        # Format response
        processing_time = time.time() - start_time
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"] if query.include_sources else [],
            confidence_score=result["confidence_score"],
            language=result["language"],
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/pyq", response_model=PYQAnalyticsResponse)
async def get_pyq_analytics():
    """Get PYQ analytics"""
    try:
        # Retrieve all documents with text content
        chroma = get_chroma_client()
        all_docs = chroma.get_all_documents()
        
        if not all_docs:
            return PYQAnalyticsResponse(
                total_questions=0,
                patterns=[],
                topic_distribution={},
                difficulty_distribution={},
                year_wise_trends={}
            )
        
        # Analyze - documents already have text and metadata
        analytics = get_pyq_analytics()
        result = analytics.analyze_questions(all_docs)
        
        return PYQAnalyticsResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge-graph", response_model=KnowledgeGraphResponse)
async def get_knowledge_graph_data():
    """Get knowledge graph"""
    try:
        # Retrieve all documents with text content
        chroma = get_chroma_client()
        all_docs = chroma.get_all_documents()
        
        if not all_docs:
            return KnowledgeGraphResponse(
                nodes=[],
                edges=[],
                statistics={"total_nodes": 0, "total_edges": 0, "density": 0}
            )
        
        # Use sample of documents for graph generation (max 20)
        documents = all_docs[:20]
        
        # Generate graph
        kg = get_knowledge_graph()
        result = kg.generate_graph(documents)
        
        return KnowledgeGraphResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/governance/stats", response_model=GovernanceStats)
async def get_governance_stats():
    """Get governance statistics"""
    try:
        governance = get_governance_panel()
        stats = governance.get_statistics()
        return GovernanceStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/governance/approve")
async def approve_document(request: DocumentApprovalRequest):
    """Approve or reject a document"""
    try:
        governance = get_governance_panel()
        
        if request.action == "approve":
            success = governance.approve_document(request.document_id)
        elif request.action == "reject":
            success = governance.reject_document(
                request.document_id,
                reason=request.reason or "Not suitable"
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {"success": True, "message": f"Document {request.action}ed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/governance/pending")
async def get_pending_documents():
    """Get pending documents"""
    try:
        governance = get_governance_panel()
        pending = governance.get_pending_documents()
        return {"documents": pending}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
