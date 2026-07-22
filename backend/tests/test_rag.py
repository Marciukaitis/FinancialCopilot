"""Tests del pipeline RAG (sin llamadas reales a OpenAI)."""

from typing import List
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from backend.app.core.exceptions import RAGError
from backend.app.rag.chains.rag_chain import RAGChain
from backend.app.rag.graph.rag_graph import RAGGraph
from backend.app.rag.retriever.document_retriever import RetrievedChunk


def _chunks() -> List[RetrievedChunk]:
    return [
        RetrievedChunk(
            document=Document(
                page_content="Operating margin was 18% in 2024.",
                metadata={"filename": "report.pdf", "page": 3},
            ),
            score=0.15,
            rank=1,
        ),
        RetrievedChunk(
            document=Document(
                page_content="Revenue grew 10% year over year.",
                metadata={"filename": "report.pdf", "page": 1},
            ),
            score=0.22,
            rank=2,
        ),
    ]


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_build_context_includes_sources(mock_chat: MagicMock) -> None:
    chain = RAGChain(api_key="test-key")
    context = chain.build_context(_chunks())

    assert "report.pdf" in context
    assert "Operating margin was 18%" in context
    assert "Revenue grew 10%" in context


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_extract_sources(mock_chat: MagicMock) -> None:
    chain = RAGChain(api_key="test-key")
    sources = chain.extract_sources(_chunks())

    assert len(sources) == 2
    assert sources[0]["filename"] == "report.pdf"
    assert sources[0]["page"] == 3


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_generate_uses_context_only_prompt(mock_chat: MagicMock) -> None:
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(content="El margen operativo fue 18%.")
    mock_chat.return_value = llm

    chain = RAGChain(api_key="test-key")
    answer = chain.generate(
        question="¿Cuál es el margen operativo?",
        context="[Fuente: report.pdf]\nOperating margin was 18%.",
    )

    assert answer == "El margen operativo fue 18%."
    llm.invoke.assert_called_once()
    messages = llm.invoke.call_args[0][0]
    serialized = " ".join(str(message.content) for message in messages)
    assert "nunca inventes" in serialized.lower() or "Nunca inventes" in serialized
    assert "español" in serialized.lower()
    assert "suficiente información" in serialized.lower()


def test_rag_chain_requires_api_key() -> None:
    with pytest.raises(RAGError, match="OPENAI_API_KEY"):
        RAGChain(api_key="")


def test_rag_graph_pipeline() -> None:
    retriever = MagicMock()
    retriever.retrieve_with_scores.return_value = _chunks()

    chain = MagicMock()
    chain.build_context.return_value = "contexto de prueba"
    chain.extract_sources.return_value = [
        {"filename": "report.pdf", "page": 3, "rank": 1, "score": 0.15}
    ]
    chain.generate.return_value = "El margen operativo fue 18%."

    graph = RAGGraph(retriever=retriever, chain=chain)
    result = graph.invoke("¿Cuál es el margen operativo?")

    retriever.retrieve_with_scores.assert_called_once_with(
        "¿Cuál es el margen operativo?"
    )
    chain.build_context.assert_called_once()
    chain.generate.assert_called_once_with(
        question="¿Cuál es el margen operativo?",
        context="contexto de prueba",
    )
    assert result.answer == "El margen operativo fue 18%."
    assert result.chunks_used == 2
    assert result.sources[0]["filename"] == "report.pdf"


def test_rag_graph_rejects_empty_query() -> None:
    graph = RAGGraph(retriever=MagicMock(), chain=MagicMock())
    with pytest.raises(RAGError, match="Query cannot be empty"):
        graph.invoke("  ")
