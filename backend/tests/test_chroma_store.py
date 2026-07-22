"""Tests de ChromaStore e IndexingService (sin OpenAI ni disco real de producción)."""

from typing import List
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from backend.app.core.exceptions import VectorStoreError
from backend.app.rag.vectorstore.chroma_store import ChromaStore
from backend.app.services.indexing_service import IndexingService


def _docs() -> List[Document]:
    return [
        Document(page_content="Revenue grew 10%.", metadata={"filename": "a.pdf"}),
        Document(page_content="Costs declined 5%.", metadata={"filename": "a.pdf"}),
    ]


@patch("backend.app.rag.vectorstore.chroma_store.Chroma")
@patch("backend.app.rag.vectorstore.chroma_store.OpenAIEmbeddings")
def test_add_documents_stores_embeddings(
    mock_embeddings: MagicMock,
    mock_chroma: MagicMock,
    tmp_path,
) -> None:
    vectorstore = MagicMock()
    vectorstore.add_documents.return_value = ["id-1", "id-2"]
    mock_chroma.return_value = vectorstore

    store = ChromaStore(
        persist_directory=str(tmp_path / "chroma"),
        collection_name="finance_documents",
        api_key="test-key",
    )
    ids = store.add_documents(_docs())

    assert ids == ["id-1", "id-2"]
    vectorstore.add_documents.assert_called_once()
    assert store.collection_name == "finance_documents"


@patch("backend.app.rag.vectorstore.chroma_store.Chroma")
@patch("backend.app.rag.vectorstore.chroma_store.OpenAIEmbeddings")
def test_reset_collection(
    mock_embeddings: MagicMock,
    mock_chroma: MagicMock,
    tmp_path,
) -> None:
    vectorstore = MagicMock()
    mock_chroma.return_value = vectorstore

    store = ChromaStore(
        persist_directory=str(tmp_path / "chroma"),
        api_key="test-key",
    )
    store.reset_collection()

    vectorstore.delete_collection.assert_called_once()
    assert mock_chroma.call_count == 2


def test_chroma_requires_api_key(tmp_path) -> None:
    with pytest.raises(VectorStoreError, match="OPENAI_API_KEY"):
        ChromaStore(
            persist_directory=str(tmp_path / "chroma"),
            api_key="",
            embeddings=None,
        )


def test_reindex_all_pipeline() -> None:
    pdf_loader = MagicMock()
    pdf_loader.load_documents.return_value = _docs()

    chunker = MagicMock()
    chunker.split_documents.return_value = _docs()

    vector_store = MagicMock()
    vector_store.collection_name = "finance_documents"
    vector_store.count.return_value = 2

    service = IndexingService(
        pdf_loader=pdf_loader,
        chunker=chunker,
        vector_store=vector_store,
    )
    result = service.reindex_all()

    vector_store.reset_collection.assert_called_once()
    vector_store.add_documents.assert_called_once_with(_docs())
    assert result.chunks_indexed == 2
    assert result.collection_name == "finance_documents"
    assert result.total_in_store == 2


def test_reindex_all_with_no_documents() -> None:
    pdf_loader = MagicMock()
    pdf_loader.load_documents.return_value = []

    chunker = MagicMock()
    chunker.split_documents.return_value = []

    vector_store = MagicMock()
    vector_store.collection_name = "finance_documents"
    vector_store.count.return_value = 0

    service = IndexingService(
        pdf_loader=pdf_loader,
        chunker=chunker,
        vector_store=vector_store,
    )
    result = service.reindex_all()

    vector_store.reset_collection.assert_called_once()
    vector_store.add_documents.assert_not_called()
    assert result.chunks_indexed == 0
