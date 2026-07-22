"""Servicio de consultas: retrieval y RAG completo."""

from typing import List, Optional

from backend.app.rag.graph.rag_graph import RAGGraph, RAGResult
from backend.app.rag.retriever.document_retriever import DocumentRetriever, RetrievedChunk


class QueryService:
    """Orquesta búsquedas semánticas y respuestas RAG."""

    def __init__(
        self,
        retriever: Optional[DocumentRetriever] = None,
        rag_graph: Optional[RAGGraph] = None,
    ) -> None:
        self._retriever = retriever
        self._rag_graph = rag_graph

    @property
    def retriever(self) -> DocumentRetriever:
        if self._retriever is None:
            self._retriever = DocumentRetriever()
        return self._retriever

    @property
    def rag_graph(self) -> RAGGraph:
        if self._rag_graph is None:
            self._rag_graph = RAGGraph(retriever=self.retriever)
        return self._rag_graph

    def retrieve(self, query: str) -> List[RetrievedChunk]:
        return self.retriever.retrieve_with_scores(query)

    def ask(self, query: str) -> RAGResult:
        """Ejecuta el pipeline completo: Retriever → Contexto → Prompt → GPT."""
        return self.rag_graph.invoke(query)
