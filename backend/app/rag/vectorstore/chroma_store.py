"""Cliente y operaciones sobre ChromaDB."""

from pathlib import Path
from typing import List, Optional

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from backend.app.config.settings import settings
from backend.app.core.exceptions import VectorStoreError


class ChromaStore:
    """Almacena embeddings en ChromaDB (colección finance_documents)."""

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: Optional[str] = None,
        embeddings: Optional[OpenAIEmbeddings] = None,
        api_key: Optional[str] = None,
        embedding_model: Optional[str] = None,
    ) -> None:
        self.persist_directory = Path(
            persist_directory or settings.CHROMA_PERSIST_DIRECTORY
        )
        self.collection_name = collection_name or settings.CHROMA_COLLECTION_NAME
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        api_key = api_key or settings.OPENAI_API_KEY
        if embeddings is None and not api_key:
            raise VectorStoreError(
                "OPENAI_API_KEY is required to store embeddings in ChromaDB."
            )

        self._embeddings = embeddings or OpenAIEmbeddings(
            model=embedding_model or settings.EMBEDDING_MODEL,
            api_key=api_key,
        )
        self._vectorstore = self._build_vectorstore()

    def _build_vectorstore(self) -> Chroma:
        try:
            return Chroma(
                collection_name=self.collection_name,
                embedding_function=self._embeddings,
                persist_directory=str(self.persist_directory),
            )
        except Exception as exc:
            raise VectorStoreError(
                f"Failed to initialize ChromaDB collection '{self.collection_name}': {exc}"
            ) from exc

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Genera embeddings y los almacena automáticamente en ChromaDB."""
        if not documents:
            return []

        try:
            ids = self._vectorstore.add_documents(documents)
        except Exception as exc:
            raise VectorStoreError(
                f"Failed to add documents to ChromaDB: {exc}"
            ) from exc

        return ids

    def reset_collection(self) -> None:
        """Elimina y recrea la colección para una reindexación completa."""
        try:
            self._vectorstore.delete_collection()
        except Exception:
            # La colección puede no existir aún
            pass

        self._vectorstore = self._build_vectorstore()

    def count(self) -> int:
        """Cantidad de vectores almacenados en la colección."""
        try:
            return self._vectorstore._collection.count()
        except Exception as exc:
            raise VectorStoreError(
                f"Failed to count documents in ChromaDB: {exc}"
            ) from exc

    def get_vectorstore(self) -> Chroma:
        return self._vectorstore
