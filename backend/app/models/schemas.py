"""Schemas Pydantic compartidos entre endpoints."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    filename: str
    path: str
    size_bytes: int
    message: str = "Document uploaded successfully"
    documents_loaded: int = 0
    chunks_indexed: int = 0
    collection_name: str = "finance_documents"


class ReindexResponse(BaseModel):
    message: str = "Documents reindexed successfully"
    documents_loaded: int
    chunks_indexed: int
    collection_name: str
    total_in_store: int


class RetrieveRequest(BaseModel):
    query: str


class RetrievedChunkResponse(BaseModel):
    rank: int
    content: str
    source: str
    score: Optional[float] = None
    metadata: Dict[str, Any]


class RetrieveResponse(BaseModel):
    query: str
    k: int
    results: List[RetrievedChunkResponse]


class QueryRequest(BaseModel):
    query: str


class SourceResponse(BaseModel):
    document: str = Field(..., description="Nombre del documento PDF")
    page: Optional[int] = Field(
        None,
        description="Número de página (1-indexado)",
    )
    rank: Optional[int] = None
    score: Optional[float] = None


class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceResponse]
    chunks_used: int
    cleaned_query: Optional[str] = None
    is_valid: bool = True
    validation_notes: List[str] = []
    analysis: Dict[str, Any] = {}
