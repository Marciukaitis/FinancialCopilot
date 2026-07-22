"""Servicio de consultas semánticas (sin LLM todavía)."""

from typing import List, Optional

from backend.app.rag.retriever.document_retriever import DocumentRetriever, RetrievedChunk


class QueryService:
    """Orquesta búsquedas semánticas sobre ChromaDB."""

    def __init__(self, retriever: Optional[DocumentRetriever] = None) -> None:
        self._retriever = retriever

    @property
    def retriever(self) -> DocumentRetriever:
        if self._retriever is None:
            self._retriever = DocumentRetriever()
        return self._retriever

    def retrieve(self, query: str) -> List[RetrievedChunk]:
        return self.retriever.retrieve_with_scores(query)
