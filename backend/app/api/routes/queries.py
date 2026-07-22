"""Endpoints de consultas semánticas y RAG."""

from fastapi import APIRouter, HTTPException

from backend.app.core.exceptions import (
    EmbeddingError,
    RAGError,
    RetrievalError,
    VectorStoreError,
)
from backend.app.models.schemas import (
    QueryRequest,
    QueryResponse,
    RetrieveRequest,
    RetrieveResponse,
    RetrievedChunkResponse,
    SourceResponse,
)
from backend.app.services.query_service import QueryService

router = APIRouter(tags=["queries"])
query_service = QueryService()

PIPELINE_ERRORS = (
    RetrievalError,
    RAGError,
    VectorStoreError,
    EmbeddingError,
)


@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_documents(payload: RetrieveRequest) -> RetrieveResponse:
    """Búsqueda semántica en ChromaDB sin generación con LLM."""
    try:
        results = query_service.retrieve(payload.query)
    except PIPELINE_ERRORS as exc:
        raise HTTPException(status_code=400, detail=exc.message) from exc

    return RetrieveResponse(
        query=payload.query,
        k=query_service.retriever.k,
        results=[
            RetrievedChunkResponse(
                rank=item.rank,
                content=item.content,
                source=item.source,
                score=item.score,
                metadata=item.metadata,
            )
            for item in results
        ],
    )


@router.post("/query", response_model=QueryResponse)
async def query_documents(payload: QueryRequest) -> QueryResponse:
    """
    Pipeline RAG con LangGraph:

    Usuario → Analizar → Buscar → Generar → Validar → Usuario
    """
    try:
        result = query_service.ask(payload.query)
    except PIPELINE_ERRORS as exc:
        raise HTTPException(status_code=400, detail=exc.message) from exc

    return QueryResponse(
        query=result.query,
        answer=result.answer,
        sources=[SourceResponse(**source) for source in result.sources],
        chunks_used=result.chunks_used,
        cleaned_query=result.cleaned_query,
        is_valid=result.is_valid,
        validation_notes=result.validation_notes,
        analysis=result.analysis,
    )
