"""Construcción de contexto y generación de respuestas con GPT."""

from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from backend.app.config.settings import settings
from backend.app.core.exceptions import RAGError
from backend.app.rag.chains.prompts import build_rag_prompt
from backend.app.rag.retriever.document_retriever import RetrievedChunk


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

    def build_context(self, chunks: List[RetrievedChunk]) -> str:
        """Une los chunks recuperados en un único bloque de contexto."""
        if not chunks:
            return "No se recuperó contexto relevante de los documentos."

        sections: List[str] = []
        for chunk in chunks:
            source = chunk.source
            page = chunk.metadata.get("page", "n/a")
            header = f"[Fuente: {source} | página: {page} | rank: {chunk.rank}]"
            sections.append(f"{header}\n{chunk.content}")

        return "\n\n".join(sections)

    def extract_sources(self, chunks: List[RetrievedChunk]) -> List[dict]:
        """Lista de fuentes únicas usadas en la respuesta."""
        seen = set()
        sources: List[dict] = []

        for chunk in chunks:
            key = (chunk.source, chunk.metadata.get("page"))
            if key in seen:
                continue
            seen.add(key)
            sources.append(
                {
                    "filename": chunk.source,
                    "page": chunk.metadata.get("page"),
                    "rank": chunk.rank,
                    "score": chunk.score,
                }
            )

        return sources

    def generate(self, question: str, context: str) -> str:
        """Invoca GPT con el prompt anclado al contexto."""
        try:
            messages: List[BaseMessage] = self._prompt.format_messages(
                context=context,
                question=question,
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
