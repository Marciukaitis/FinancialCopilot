"""Retriever semántico sobre ChromaDB (sin LLM)."""

from dataclasses import dataclass
from typing import List, Optional, Tuple

from langchain_core.documents import Document

from backend.app.config.settings import settings
from backend.app.core.exceptions import RetrievalError
from backend.app.rag.vectorstore.chroma_store import ChromaStore


@dataclass
class RetrievedChunk:
    """Resultado de una búsqueda semántica."""

    document: Document
    score: Optional[float]
    rank: int

    @property
    def content(self) -> str:
        return self.document.page_content

    @property
    def metadata(self) -> dict:
        return self.document.metadata

    @property
    def source(self) -> str:
        return str(
            self.metadata.get("filename")
            or self.metadata.get("source")
            or "unknown"
        )


class DocumentRetriever:
    """Busca chunks relevantes únicamente en ChromaDB."""

    def __init__(
        self,
        vector_store: Optional[ChromaStore] = None,
        k: Optional[int] = None,
    ) -> None:
        self.vector_store = vector_store or ChromaStore()
        self.k = k if k is not None else settings.RETRIEVER_K
        self._retriever = self.vector_store.get_vectorstore().as_retriever(
            search_kwargs={"k": self.k}
        )

    def retrieve(self, query: str) -> List[Document]:
        """Devuelve los k documentos más similares a la consulta."""
        query = (query or "").strip()
        if not query:
            raise RetrievalError("Query cannot be empty.")

        try:
            return self._retriever.invoke(query)
        except Exception as exc:
            raise RetrievalError(f"Failed to retrieve documents: {exc}") from exc

    def retrieve_with_scores(self, query: str) -> List[RetrievedChunk]:
        """Devuelve documentos con score de similitud (menor distancia = más similar)."""
        query = (query or "").strip()
        if not query:
            raise RetrievalError("Query cannot be empty.")

        try:
            results: List[Tuple[Document, float]] = (
                self.vector_store.get_vectorstore().similarity_search_with_score(
                    query,
                    k=self.k,
                )
            )
        except Exception as exc:
            raise RetrievalError(f"Failed to retrieve documents: {exc}") from exc

        return [
            RetrievedChunk(document=document, score=score, rank=index)
            for index, (document, score) in enumerate(results, start=1)
        ]

    def print_results(self, query: str, results: List[RetrievedChunk]) -> None:
        """Imprime resultados de búsqueda semántica por consola."""
        print(f"\nQuery: {query}")
        print(f"k={self.k} | resultados={len(results)}")
        print(f"colección={self.vector_store.collection_name}\n")
        print("=" * 60)

        if not results:
            print("No se encontraron documentos relevantes.")
            return

        for item in results:
            preview = item.content[:200].replace("\n", " ")
            score_text = f"{item.score:.4f}" if item.score is not None else "n/a"
            print(f"[#{item.rank}] source={item.source} | score={score_text}")
            print(preview)
            if len(item.content) > 200:
                print("...")
            print("-" * 60)
