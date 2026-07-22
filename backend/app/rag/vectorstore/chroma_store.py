"""Cliente y operaciones sobre ChromaDB (embeddings locales)."""

from pathlib import Path
from typing import List, Optional

import chromadb
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from backend.app.config.settings import settings
from backend.app.core.exceptions import EmbeddingError, VectorStoreError
from backend.app.rag.embeddings.factory import build_embeddings


class ChromaStore:
    """Almacena embeddings en ChromaDB (colección finance_documents)."""

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: Optional[str] = None,
        embeddings: Optional[HuggingFaceEmbeddings] = None,
        embedding_model: Optional[str] = None,
    ) -> None:
        self.persist_directory = Path(
            persist_directory or settings.CHROMA_PERSIST_DIRECTORY
        )
        self.collection_name = collection_name or settings.CHROMA_COLLECTION_NAME
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        try:
            self._embeddings = embeddings or build_embeddings(
                embedding_model or settings.EMBEDDING_MODEL
            )
        except EmbeddingError as exc:
            raise VectorStoreError(exc.message) from exc

        self._vectorstore = self._build_vectorstore()

    def _client(self) -> chromadb.PersistentClient:
        return chromadb.PersistentClient(path=str(self.persist_directory))

    def _build_vectorstore(self) -> Chroma:
        try:
            return Chroma(
                collection_name=self.collection_name,
                embedding_function=self._embeddings,
                persist_directory=str(self.persist_directory),
                client=self._client(),
            )
        except Exception as exc:
            raise VectorStoreError(
                f"Failed to initialize ChromaDB collection '{self.collection_name}': {exc}"
            ) from exc

    def _collection_exists(self) -> bool:
        try:
            names = {item.name for item in self._client().list_collections()}
            return self.collection_name in names
        except Exception:
            return False

    def ensure_collection(self) -> Chroma:
        """Reabre la colección si fue borrada o quedó inconsistente."""
        try:
            if not self._collection_exists():
                self._vectorstore = self._build_vectorstore()
            else:
                # Verifica que el handle interno siga válido
                _ = self._vectorstore._collection.count()
        except Exception:
            self._vectorstore = self._build_vectorstore()

        return self._vectorstore

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Genera embeddings locales y los almacena en ChromaDB."""
        if not documents:
            return []

        try:
            store = self.ensure_collection()
            ids = store.add_documents(documents)
        except Exception as exc:
            raise VectorStoreError(
                f"Failed to add documents to ChromaDB: {exc}"
            ) from exc

        return ids

    def reset_collection(self) -> None:
        """Elimina y recrea la colección para una reindexación completa."""
        try:
            self._client().delete_collection(name=self.collection_name)
        except Exception:
            pass

        try:
            if hasattr(self, "_vectorstore") and self._vectorstore is not None:
                self._vectorstore.delete_collection()
        except Exception:
            pass

        self._vectorstore = self._build_vectorstore()

    def count(self) -> int:
        """Cantidad de vectores almacenados en la colección."""
        try:
            return self.ensure_collection()._collection.count()
        except Exception as exc:
            raise VectorStoreError(
                f"Failed to count documents in ChromaDB: {exc}"
            ) from exc

    def get_vectorstore(self) -> Chroma:
        return self.ensure_collection()
