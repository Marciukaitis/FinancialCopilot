"""Tests del EmbeddingService local (sin cargar el modelo real)."""

from typing import List
from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from backend.app.rag.embeddings.huggingface_embeddings import EmbeddingService


def _chunks() -> List[Document]:
    return [
        Document(page_content="Revenue grew 10%.", metadata={"filename": "a.pdf"}),
        Document(page_content="Costs declined 5%.", metadata={"filename": "a.pdf"}),
    ]


@patch("backend.app.rag.embeddings.huggingface_embeddings.build_embeddings")
def test_embed_chunks_returns_one_vector_per_chunk(mock_build: MagicMock) -> None:
    mock_instance = MagicMock()
    mock_instance.embed_documents.return_value = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]
    mock_build.return_value = mock_instance

    service = EmbeddingService(model="sentence-transformers/all-MiniLM-L6-v2")
    result = service.embed_chunks(_chunks())

    assert len(result) == 2
    assert result[0].dimensions == 3
    assert result[0].embedding == [0.1, 0.2, 0.3]
    assert result[1].content == "Costs declined 5%."
    mock_instance.embed_documents.assert_called_once()


@patch("backend.app.rag.embeddings.huggingface_embeddings.build_embeddings")
def test_embed_empty_list(mock_build: MagicMock) -> None:
    mock_build.return_value = MagicMock()
    service = EmbeddingService()
    assert service.embed_chunks([]) == []


@patch("backend.app.rag.embeddings.huggingface_embeddings.build_embeddings")
def test_print_embeddings(mock_build: MagicMock, capsys) -> None:
    mock_instance = MagicMock()
    mock_instance.embed_documents.return_value = [[0.1, 0.2, 0.3]]
    mock_build.return_value = mock_instance

    service = EmbeddingService()
    embedded = service.embed_chunks(_chunks()[:1])
    service.print_embeddings(embedded)

    output = capsys.readouterr().out
    assert "Total embeddings: 1" in output
    assert "dims=3" in output
