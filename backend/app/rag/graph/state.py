"""Estado y resultado del grafo RAG con LangGraph."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TypedDict

from backend.app.rag.retriever.document_retriever import RetrievedChunk


class RAGState(TypedDict, total=False):
    """Estado compartido entre los nodos del StateGraph."""

    # Entrada
    query: str

    # Nodo 1 — Analizar pregunta
    cleaned_query: str
    analysis: Dict[str, Any]

    # Nodo 2 — Buscar documentos
    chunks: List[RetrievedChunk]
    context: str
    sources: List[Dict[str, Any]]

    # Nodo 3 — Generar respuesta
    answer: str

    # Nodo 4 — Validar respuesta
    is_valid: bool
    validation_notes: List[str]


@dataclass
class RAGResult:
    """Resultado final expuesto al resto de la aplicación."""

    query: str
    answer: str
    context: str
    sources: List[Dict[str, Any]] = field(default_factory=list)
    chunks_used: int = 0
    cleaned_query: str = ""
    analysis: Dict[str, Any] = field(default_factory=dict)
    is_valid: bool = True
    validation_notes: List[str] = field(default_factory=list)
