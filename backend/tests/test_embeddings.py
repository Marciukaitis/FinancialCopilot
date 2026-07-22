"""Tests del EmbeddingService (sin llamadas reales a OpenAI)."""

from typing import List
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from backend.app.core.exceptions import EmbeddingError
from backend.app.rag.embeddings.openai_embeddings import EmbeddingService


def _chunks() -> List[Document]:
    return [
        Document(page_content="Revenue grew 10%.", metadata={"filename": "a.pdf"}),
        Document(page_content="Costs declined 5%.", metadata={"filename": "a.pdf"}),
    ]


def test_embed_chunks_requires_api_key() -> None:
    with pytest.raises(EmbeddingError, match="OPENAI_API_KEY"):
        EmbeddingService(api_key="")


@patch("backend.app.rag.embeddings.openai_embeddings.OpenAIEmbeddings")
def test_embed_chunks_returns_one_vector_per_chunk(mock_openai: MagicMock) -> None:
    mock_instance = MagicMock()
    mock_instance.embed_documents.return_value = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]
    mock_openai.return_value = mock_instance

    service = EmbeddingService(api_key="test-key", model="text-embedding-3-small")
    result = service.embed_chunks(_chunks())

    assert len(result) == 2
    assert result[0].dimensions == 3
    assert result[0].embedding == [0.1, 0.2, 0.3]
    assert result[1].content == "Costs declined 5%."
    mock_instance.embed_documents.assert_called_once()


@patch("backend.app.rag.embeddings.openai_embeddings.OpenAIEmbeddings")
def test_embed_empty_list(mock_openai: MagicMock) -> None:
    mock_openai.return_value = MagicMock()
    service = EmbeddingService(api_key="test-key")
    assert service.embed_chunks([]) == []


@patch("backend.app.rag.embeddings.openai_embeddings.OpenAIEmbeddings")
def test_print_embeddings(mock_openai: MagicMock, capsys) -> None:
    mock_instance = MagicMock()
    mock_instance.embed_documents.return_value = [[0.1, 0.2, 0.3]]
    mock_openai.return_value = mock_instance

    service = EmbeddingService(api_key="test-key")
    embedded = service.embed_chunks(_chunks()[:1])
    service.print_embeddings(embedded)

    output = capsys.readouterr().out
    assert "Total embeddings: 1" in output
    assert "dims=3" in output
