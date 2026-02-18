"""
Pydantic models for request/response schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentMetadata(BaseModel):
    """Metadata for uploaded documents"""
    filename: str
    file_type: str
    upload_date: datetime = Field(default_factory=datetime.now)
    total_pages: Optional[int] = None
    total_chunks: Optional[int] = None


class UploadResponse(BaseModel):
    """Response after document upload"""
    success: bool
    message: str
    document_id: str
    metadata: Optional[DocumentMetadata] = None


class ChatQuery(BaseModel):
    """Chat query request"""
    query: str
    language: str = "en"
    top_k: int = 5
    include_sources: bool = True


class SourceDocument(BaseModel):
    """Source document reference"""
    filename: str
    page: Optional[int] = None
    chunk_text: str
    relevance_score: float


class ChatResponse(BaseModel):
    """Chat response with RAG results"""
    answer: str
    sources: List[SourceDocument]
    confidence_score: float
    language: str
    processing_time: float


class PYQPattern(BaseModel):
    """Pattern detected in PYQ analysis"""
    topic: str
    frequency: int
    years: List[int]
    difficulty: str
    importance_score: float


class PYQAnalyticsResponse(BaseModel):
    """PYQ analytics results"""
    total_questions: int
    patterns: List[PYQPattern]
    topic_distribution: Dict[str, int]
    difficulty_distribution: Dict[str, int]
    year_wise_trends: Dict[str, int]


class GraphNode(BaseModel):
    """Node in knowledge graph"""
    id: str
    label: str
    type: str  # entity, topic, concept
    properties: Dict[str, Any] = {}


class GraphEdge(BaseModel):
    """Edge in knowledge graph"""
    source: str
    target: str
    relationship: str
    weight: float = 1.0


class KnowledgeGraphResponse(BaseModel):
    """Knowledge graph structure"""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    statistics: Dict[str, Any]


class DocumentApprovalRequest(BaseModel):
    """Request to approve/reject document"""
    document_id: str
    action: str  # "approve" or "reject"
    reason: Optional[str] = None


class GovernanceStats(BaseModel):
    """Governance panel statistics"""
    total_documents: int
    pending_approval: int
    approved_documents: int
    rejected_documents: int
    total_queries: int
    active_users: int
    storage_used_mb: float


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    ollama_status: str
    chroma_status: str
    timestamp: datetime = Field(default_factory=datetime.now)
