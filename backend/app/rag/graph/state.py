"""Estado y resultado del grafo RAG con memoria conversacional."""

from dataclasses import dataclass, field
from typing import Annotated, Any, Dict, List, TypedDict

from backend.app.rag.retriever.document_retriever import RetrievedChunk


def append_history(
    existing: List[Dict[str, str]],
    new: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    """Reducer de LangGraph: acumula turnos de la conversación."""
    return (existing or []) + (new or [])


class RAGState(TypedDict, total=False):
    """Estado compartido entre los nodos del StateGraph."""

    # Entrada
    query: str

    # Memoria conversacional (persistida por thread_id)
    conversation_history: Annotated[List[Dict[str, str]], append_history]

    # Nodo 1 — Analizar pregunta
    cleaned_query: str
    search_query: str
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
    thread_id: str
    sources: List[Dict[str, Any]] = field(default_factory=list)
    retrieved_chunks: List[Dict[str, Any]] = field(default_factory=list)
    chunks_used: int = 0
    cleaned_query: str = ""
    search_query: str = ""
    analysis: Dict[str, Any] = field(default_factory=dict)
    is_valid: bool = True
    validation_notes: List[str] = field(default_factory=list)
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
