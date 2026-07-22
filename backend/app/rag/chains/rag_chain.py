"""Construcción de contexto y generación de respuestas con GPT."""

from typing import Any, Dict, List, Optional

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from backend.app.config.settings import settings
from backend.app.core.exceptions import RAGError
from backend.app.rag.chains.prompts import build_followup_rewrite_prompt, build_rag_prompt
from backend.app.rag.retriever.document_retriever import RetrievedChunk

INSUFFICIENT_INFO_MARKERS = (
    "no poseo suficiente información",
    "no encontré información suficiente",
)


class RAGChain:
    """Formatea el contexto y genera la respuesta con GPT."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> None:
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.LLM_MODEL
        self.temperature = (
            temperature if temperature is not None else settings.LLM_TEMPERATURE
        )

        if not self.api_key:
            raise RAGError("OPENAI_API_KEY is required to run the RAG pipeline.")

        self._llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            api_key=self.api_key,
        )
        self._prompt = build_rag_prompt()
        self._followup_prompt = build_followup_rewrite_prompt()
        self.max_history_turns = settings.CONVERSATION_HISTORY_TURNS

    @staticmethod
    def normalize_page(page: Any) -> Optional[int]:
        """Convierte la página de PyPDF (0-index) a número legible (1-index)."""
        if page is None or page == "n/a":
            return None
        try:
            page_number = int(page)
        except (TypeError, ValueError):
            return None
        return page_number + 1 if page_number >= 0 else page_number

    def build_context(self, chunks: List[RetrievedChunk]) -> str:
        """Une los chunks recuperados en un único bloque de contexto."""
        if not chunks:
            return "No se recuperó contexto relevante de los documentos."

        sections: List[str] = []
        for chunk in chunks:
            document = chunk.source
            page = self.normalize_page(chunk.metadata.get("page"))
            page_label = str(page) if page is not None else "desconocida"
            header = (
                f"[Documento: {document} | Página: {page_label} | rank: {chunk.rank}]"
            )
            sections.append(f"{header}\n{chunk.content}")

        return "\n\n".join(sections)

    def format_chat_history(self, history: List[Dict[str, str]]) -> str:
        """Serializa el historial reciente para el prompt."""
        if not history:
            return "(Sin historial previo)"

        recent = history[-(self.max_history_turns * 2) :]
        lines: List[str] = []
        for turn in recent:
            role = turn.get("role", "user")
            label = "Usuario" if role == "user" else "Asistente"
            content = (turn.get("content") or "").strip()
            if content:
                lines.append(f"{label}: {content}")

        return "\n".join(lines) if lines else "(Sin historial previo)"

    def extract_sources(self, chunks: List[RetrievedChunk]) -> List[Dict[str, Any]]:
        """Lista de fuentes únicas (documento + página)."""
        seen = set()
        sources: List[Dict[str, Any]] = []

        for chunk in chunks:
            document = chunk.source
            page = self.normalize_page(chunk.metadata.get("page"))
            key = (document, page)
            if key in seen:
                continue
            seen.add(key)
            sources.append(
                {
                    "document": document,
                    "page": page,
                    "rank": chunk.rank,
                    "score": chunk.score,
                }
            )

        return sources

    def format_sources_section(self, sources: List[Dict[str, Any]]) -> str:
        """Bloque de fuentes obligatorio para la respuesta final."""
        if not sources:
            return ""

        lines = ["", "---", "Fuentes:"]
        for source in sources:
            document = source.get("document") or "desconocido"
            page = source.get("page")
            page_label = str(page) if page is not None else "desconocida"
            lines.append(f"- Documento: {document} | Página: {page_label}")

        return "\n".join(lines)

    def attach_sources(self, answer: str, sources: List[Dict[str, Any]]) -> str:
        """Garantiza que la respuesta incluya documento y página."""
        answer = (answer or "").strip()
        if not sources:
            return answer

        if any(marker in answer.lower() for marker in INSUFFICIENT_INFO_MARKERS):
            return answer

        sources_section = self.format_sources_section(sources)
        if "fuentes:" in answer.lower():
            return answer

        return f"{answer}{sources_section}"

    def rewrite_followup_query(
        self,
        question: str,
        history: List[Dict[str, str]],
    ) -> str:
        """Reescribe una pregunta de seguimiento como consulta independiente."""
        try:
            messages: List[BaseMessage] = self._followup_prompt.format_messages(
                chat_history=self.format_chat_history(history),
                question=question,
            )
            response = self._llm.invoke(messages)
        except Exception as exc:
            raise RAGError(f"Failed to rewrite follow-up query: {exc}") from exc

        content = response.content
        if isinstance(content, list):
            content = "".join(str(part) for part in content)

        rewritten = str(content).strip().strip('"').strip("'")
        return rewritten or question

    def generate(
        self,
        question: str,
        context: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Invoca GPT con el prompt anclado al contexto y la memoria."""
        try:
            messages: List[BaseMessage] = self._prompt.format_messages(
                context=context,
                question=question,
                chat_history=self.format_chat_history(chat_history or []),
            )
            response = self._llm.invoke(messages)
        except Exception as exc:
            raise RAGError(f"Failed to generate RAG answer: {exc}") from exc

        content = response.content
        if isinstance(content, list):
            content = "".join(str(part) for part in content)

        return str(content).strip()

    def documents_to_chunks(self, documents: List[Document]) -> List[RetrievedChunk]:
        """Adapta Documents planos a RetrievedChunk (sin score)."""
        return [
            RetrievedChunk(document=document, score=None, rank=index)
            for index, document in enumerate(documents, start=1)
        ]
