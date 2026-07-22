"""Endpoints de carga e indexación de documentos."""

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.core.exceptions import (
    InvalidDocumentError,
    PDFLoadError,
    VectorStoreError,
)
from backend.app.models.schemas import ReindexResponse, StatusResponse, UploadResponse
from backend.app.services.document_service import DocumentService
from backend.app.services.indexing_service import IndexingService

router = APIRouter(tags=["documents"])
document_service = DocumentService()
indexing_service = IndexingService()


@router.get("/status", response_model=StatusResponse)
async def get_index_status() -> StatusResponse:
    """Indicador de documentos disponibles e indexados."""
    status = indexing_service.get_status()
    return StatusResponse(
        documents_count=status.documents_count,
        chunks_indexed=status.chunks_indexed,
        collection_name=status.collection_name,
        documents=status.documents,
        embedding_model=status.embedding_model,
        llm_model=status.llm_model,
        vector_db=status.vector_db,
        indexed=status.indexed,
        status="ok" if status.indexed else "pending",
    )


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    try:
        saved_path = document_service.save_pdf(file)
    except InvalidDocumentError as exc:
        raise HTTPException(status_code=400, detail=exc.message) from exc

    try:
        indexing_result = indexing_service.reindex_all()
    except (PDFLoadError, VectorStoreError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document saved but indexing failed: {exc.message}",
        ) from exc

    return UploadResponse(
        filename=saved_path.name,
        path=str(saved_path),
        size_bytes=saved_path.stat().st_size,
        documents_loaded=indexing_result.documents_loaded,
        chunks_indexed=indexing_result.chunks_indexed,
        collection_name=indexing_result.collection_name,
    )


@router.post("/reindex", response_model=ReindexResponse)
async def reindex_documents() -> ReindexResponse:
    """Reindexa todos los PDFs existentes en data/documents."""
    try:
        result = indexing_service.reindex_all()
    except (PDFLoadError, VectorStoreError) as exc:
        raise HTTPException(status_code=500, detail=exc.message) from exc

    return ReindexResponse(
        documents_loaded=result.documents_loaded,
        chunks_indexed=result.chunks_indexed,
        collection_name=result.collection_name,
        total_in_store=result.total_in_store,
    )
