"""Nodos del StateGraph RAG con memoria conversacional."""

from typing import Any, Dict, List

from backend.app.rag.chains.rag_chain import INSUFFICIENT_INFO_MARKERS, RAGChain
from backend.app.rag.graph.state import RAGState
from backend.app.rag.retriever.document_retriever import DocumentRetriever

INSUFFICIENT_INFO_MESSAGE = (
    "No poseo suficiente información en los documentos disponibles "
    "para responder esta pregunta."
)

FOLLOWUP_PREFIXES = (
    "y ",
    "¿y ",
    "and ",
    "entonces ",
    "¿entonces ",
    "respecto ",
    "¿respecto ",
    "en ese ",
    "¿en ese ",
    "de eso",
    "¿de eso",
)


class RAGNodes:
    """
    Nodos del flujo:

    1. analyze_question
    2. search_documents
    3. generate_answer
    4. validate_answer
    """

    def __init__(self, retriever: DocumentRetriever, chain: RAGChain) -> None:
        self.retriever = retriever
        self.chain = chain

    def analyze_question(self, state: RAGState) -> RAGState:
        """Nodo 1: normaliza la pregunta y resuelve referencias del historial."""
        raw_query = (state.get("query") or "").strip()
        cleaned_query = " ".join(raw_query.split())
        history = state.get("conversation_history") or []
        is_followup = self._is_followup(cleaned_query, history)

        search_query = cleaned_query
        if is_followup and history:
            search_query = self.chain.rewrite_followup_query(cleaned_query, history)

        analysis: Dict[str, Any] = {
            "original_query": raw_query,
            "character_count": len(cleaned_query),
            "word_count": len(cleaned_query.split()) if cleaned_query else 0,
            "is_question": "?" in cleaned_query,
            "is_followup": is_followup,
            "history_turns": len(history),
            "language_hint": "es",
            "intent": self._infer_intent(cleaned_query),
        }

        return {
            "cleaned_query": cleaned_query,
            "search_query": search_query,
            "analysis": analysis,
        }

    def search_documents(self, state: RAGState) -> RAGState:
        """Nodo 2: busca documentos relevantes en ChromaDB."""
        search_query = (
            state.get("search_query")
            or state.get("cleaned_query")
            or state.get("query")
            or ""
        )
        chunks = self.retriever.retrieve_with_scores(search_query)
        context = self.chain.build_context(chunks)
        sources = self.chain.extract_sources(chunks)

        return {
            "chunks": chunks,
            "context": context,
            "sources": sources,
        }

    def generate_answer(self, state: RAGState) -> RAGState:
        """Nodo 3: genera la respuesta con GPT usando contexto + memoria."""
        question = state.get("cleaned_query") or state.get("query") or ""
        context = state.get("context") or ""
        sources = state.get("sources") or []
        chunks = state.get("chunks") or []
        history = state.get("conversation_history") or []

        if not chunks:
            return {"answer": INSUFFICIENT_INFO_MESSAGE}

        raw_answer = self.chain.generate(
            question=question,
            context=context,
            chat_history=history,
        )
        answer = self.chain.attach_sources(answer=raw_answer, sources=sources)
        return {"answer": answer}

    def validate_answer(self, state: RAGState) -> RAGState:
        """Nodo 4: valida la respuesta y guarda el turno en memoria."""
        answer = (state.get("answer") or "").strip()
        sources = state.get("sources") or []
        chunks = state.get("chunks") or []
        query = state.get("cleaned_query") or state.get("query") or ""
        notes: List[str] = []

        if not answer:
            answer = INSUFFICIENT_INFO_MESSAGE
            notes.append("Respuesta vacía: se reemplazó por mensaje de información insuficiente.")

        has_insufficient_info = any(
            marker in answer.lower() for marker in INSUFFICIENT_INFO_MARKERS
        )

        if not chunks:
            answer = INSUFFICIENT_INFO_MESSAGE
            notes.append("Sin documentos recuperados: no se permite inventar una respuesta.")
            return {
                "answer": answer,
                "is_valid": True,
                "validation_notes": notes,
                "conversation_history": [
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": answer},
                ],
            }

        if has_insufficient_info:
            notes.append("El modelo indicó falta de información en el contexto.")
            return {
                "answer": answer,
                "is_valid": True,
                "validation_notes": notes,
                "conversation_history": [
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": answer},
                ],
            }

        answer = self.chain.attach_sources(answer=answer, sources=sources)
        if sources and "documento:" not in answer.lower():
            notes.append("Se anexaron fuentes porque la respuesta no citaba documento.")
        if sources and "página:" not in answer.lower():
            notes.append("Se anexaron fuentes porque la respuesta no citaba página.")

        if sources and "documento:" in answer.lower() and "página:" in answer.lower():
            notes.append("Validación OK: respuesta con documento y página.")
            is_valid = True
        elif not sources:
            answer = INSUFFICIENT_INFO_MESSAGE
            notes.append("Sin fuentes disponibles: respuesta invalidada.")
            is_valid = True
        else:
            notes.append("Validación parcial: se forzaron las citas de fuentes.")
            is_valid = True

        return {
            "answer": answer,
            "is_valid": is_valid,
            "validation_notes": notes,
            "conversation_history": [
                {"role": "user", "content": query},
                {"role": "assistant", "content": answer},
            ],
        }

    @staticmethod
    def _is_followup(query: str, history: List[Dict[str, str]]) -> bool:
        if not history:
            return False

        lowered = query.lower().strip()
        if any(lowered.startswith(prefix) for prefix in FOLLOWUP_PREFIXES):
            return True

        word_count = len(lowered.split())
        if word_count <= 6 and any(
            token in lowered
            for token in ("el", "la", "los", "las", "ese", "esa", "eso", "su", "sus")
        ):
            return True

        return word_count <= 4

    @staticmethod
    def _infer_intent(query: str) -> str:
        lowered = query.lower()
        if not query:
            return "empty"
        financial_terms = (
            "margen",
            "ingreso",
            "revenue",
            "ebitda",
            "balance",
            "activo",
            "pasivo",
            "flujo",
            "costo",
            "utilidad",
            "plazo",
            "monto",
            "interés",
            "tasa",
        )
        if any(term in lowered for term in financial_terms):
            return "financial_lookup"
        if any(word in lowered for word in ("qué", "cuál", "cuánto", "cómo", "where", "what")):
            return "factual_question"
        return "general_query"
