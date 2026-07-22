"""Servicio de indexación: carga, chunking, embeddings y persistencia en ChromaDB."""

from dataclasses import dataclass
from typing import Optional

from backend.app.core.exceptions import EmbeddingError, PDFLoadError, VectorStoreError
from backend.app.rag.ingestion.pdf_loader import PDFDocumentLoader
from backend.app.rag.ingestion.text_splitter import DocumentChunker
from backend.app.rag.vectorstore.chroma_store import ChromaStore


@dataclass
class IndexingResult:
    documents_loaded: int
    chunks_indexed: int
    collection_name: str
    total_in_store: int


class IndexingService:
    """Orquesta la indexación completa de PDFs en ChromaDB."""

    def __init__(
        self,
        pdf_loader: Optional[PDFDocumentLoader] = None,
        chunker: Optional[DocumentChunker] = None,
        vector_store: Optional[ChromaStore] = None,
    ) -> None:
        self.pdf_loader = pdf_loader or PDFDocumentLoader()
        self.chunker = chunker or DocumentChunker()
        self._vector_store = vector_store

    @property
    def vector_store(self) -> ChromaStore:
        if self._vector_store is None:
            self._vector_store = ChromaStore()
        return self._vector_store

    def reindex_all(self) -> IndexingResult:
        """
        Indexa nuevamente todos los PDFs de data/documents.

        Borra la colección actual, regenera embeddings y los almacena
        en finance_documents.
        """
        try:
            documents = self.pdf_loader.load_documents()
        except PDFLoadError:
            raise

        chunks = self.chunker.split_documents(documents)

        try:
            self.vector_store.reset_collection()
            if chunks:
                self.vector_store.add_documents(chunks)
            total = self.vector_store.count()
        except (VectorStoreError, EmbeddingError):
            raise
        except Exception as exc:
            raise VectorStoreError(f"Failed to reindex documents: {exc}") from exc

        return IndexingResult(
            documents_loaded=len(documents),
            chunks_indexed=len(chunks),
            collection_name=self.vector_store.collection_name,
            total_in_store=total,
        )
