"""Schemas Pydantic compartidos entre endpoints."""

from pydantic import BaseModel


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
