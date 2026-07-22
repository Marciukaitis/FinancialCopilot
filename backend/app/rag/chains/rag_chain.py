"""Construcción de contexto y generación de respuestas con Ollama."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama

from backend.app.config.settings import settings
from backend.app.core.exceptions import RAGError
from backend.app.rag.chains.prompts import build_followup_rewrite_prompt, build_rag_prompt
from backend.app.rag.retriever.document_retriever import RetrievedChunk

INSUFFICIENT_INFO_MARKERS = (
    "no poseo suficiente información",
    "no encontré información suficiente",
)


class RAGChain:
    """Formatea el contexto y genera la respuesta con Ollama (Llama 3.2)."""

    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: Optional[float] = None,
        llm: Optional[ChatOllama] = None,
    ) -> None:
        self.model = model or settings.OLLAMA_MODEL
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.temperature = (
            temperature if temperature is not None else settings.LLM_TEMPERATURE
        )

        self._llm = llm or ChatOllama(
            model=self.model,
            base_url=self.base_url,
            temperature=self.temperature,
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
            document = self.normalize_document_name(chunk.source)
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

    @staticmethod
    def normalize_document_name(name: str) -> str:
        """Quita prefijos UUID de re-uploads: '{hex32}_archivo.pdf' → 'archivo.pdf'."""
        raw = Path(str(name or "")).name
        if len(raw) > 33 and raw[32] == "_" and all(
            ch in "0123456789abcdef" for ch in raw[:32].lower()
        ):
            return raw[33:]
        return raw

    def extract_sources(self, chunks: List[RetrievedChunk]) -> List[Dict[str, Any]]:
        """Una fuente por chunk recuperado, sin duplicar el mismo documento+página."""
        seen = set()
        sources: List[Dict[str, Any]] = []

        for chunk in chunks:
            document = self.normalize_document_name(chunk.source)
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
        """Bloque textual de fuentes (legacy / API sin UI)."""
        if not sources:
            return ""

        lines = ["", "---", "Fuentes:"]
        for source in sources:
            document = source.get("document") or "desconocido"
            page = source.get("page")
            page_label = str(page) if page is not None else "desconocida"
            lines.append(f"- Documento: {document} | Página: {page_label}")

        return "\n".join(lines)

    def strip_sources_section(self, answer: str) -> str:
        """Quita el bloque 'Fuentes:' del texto; la UI las muestra por separado."""
        text = (answer or "").strip()
        if not text:
            return ""

        markers = ("\n---\nFuentes:", "\nFuentes:", "\n**Fuentes:**")
        lower = text.lower()
        cut_at = None
        for marker in markers:
            idx = lower.find(marker.lower())
            if idx != -1 and (cut_at is None or idx < cut_at):
                cut_at = idx

        if cut_at is not None:
            text = text[:cut_at].rstrip()

        return text

    def attach_sources(self, answer: str, sources: List[Dict[str, Any]]) -> str:
        """Limpia la respuesta: las fuentes van en el campo `sources` de la API."""
        del sources  # Las fuentes estructuradas se exponen aparte en la respuesta HTTP.
        return self.strip_sources_section(answer)

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
            raise RAGError(
                "Failed to rewrite follow-up query. "
                f"Verificá que Ollama esté corriendo ({self.base_url}) "
                f"y que el modelo '{self.model}' esté instalado "
                f"(`ollama pull {self.model}`). Detalle: {exc}"
            ) from exc

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
        """Invoca Ollama con el prompt anclado al contexto y la memoria."""
        try:
            messages: List[BaseMessage] = self._prompt.format_messages(
                context=context,
                question=question,
                chat_history=self.format_chat_history(chat_history or []),
            )
            response = self._llm.invoke(messages)
        except Exception as exc:
            raise RAGError(
                "Failed to generate RAG answer. "
                f"Verificá que Ollama esté corriendo ({self.base_url}) "
                f"y que el modelo '{self.model}' esté instalado "
                f"(`ollama pull {self.model}`). Detalle: {exc}"
            ) from exc

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
