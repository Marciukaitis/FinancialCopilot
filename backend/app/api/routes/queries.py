"""Endpoints de consultas semánticas y RAG."""

from fastapi import APIRouter, HTTPException

from backend.app.core.exceptions import RAGError, RetrievalError
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


@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_documents(payload: RetrieveRequest) -> RetrieveResponse:
    """Búsqueda semántica en ChromaDB sin generación con LLM."""
    try:
        results = query_service.retrieve(payload.query)
    except RetrievalError as exc:
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
    Pipeline RAG completo:

    Usuario → Retriever → Contexto → Prompt → GPT → Respuesta
    """
    try:
        result = query_service.ask(payload.query)
    except (RetrievalError, RAGError) as exc:
        raise HTTPException(status_code=400, detail=exc.message) from exc

    return QueryResponse(
        query=result.query,
        answer=result.answer,
        sources=[SourceResponse(**source) for source in result.sources],
        chunks_used=result.chunks_used,
    )
