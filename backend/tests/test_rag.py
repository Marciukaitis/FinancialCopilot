"""Tests del pipeline RAG con LangGraph (sin llamadas reales a OpenAI)."""

from typing import List
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from backend.app.core.exceptions import RAGError
from backend.app.rag.chains.rag_chain import RAGChain
from backend.app.rag.graph.nodes import INSUFFICIENT_INFO_MESSAGE, RAGNodes
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

    assert "Documento: report.pdf" in context
    assert "Página: 4" in context
    assert "Operating margin was 18%" in context


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_extract_sources_returns_document_and_page(mock_chat: MagicMock) -> None:
    chain = RAGChain(api_key="test-key")
    sources = chain.extract_sources(_chunks())

    assert len(sources) == 2
    assert sources[0]["document"] == "report.pdf"
    assert sources[0]["page"] == 4


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_attach_sources_appends_document_and_page(mock_chat: MagicMock) -> None:
    chain = RAGChain(api_key="test-key")
    sources = [{"document": "report.pdf", "page": 4}]
    answer = chain.attach_sources("El margen operativo fue 18%.", sources)

    assert "Documento: report.pdf" in answer
    assert "Página: 4" in answer


def test_analyze_question_node() -> None:
    nodes = RAGNodes(retriever=MagicMock(), chain=MagicMock())
    result = nodes.analyze_question({"query": "  ¿Cuál es el margen?  "})

    assert result["cleaned_query"] == "¿Cuál es el margen?"
    assert result["analysis"]["intent"] == "financial_lookup"
    assert result["analysis"]["is_question"] is True


def test_validate_answer_requires_sources() -> None:
    chain = MagicMock()
    chain.attach_sources.side_effect = (
        lambda answer, sources: f"{answer}\n\n---\nFuentes:\n"
        f"- Documento: {sources[0]['document']} | Página: {sources[0]['page']}"
    )
    nodes = RAGNodes(retriever=MagicMock(), chain=chain)

    result = nodes.validate_answer(
        {
            "answer": "El margen operativo fue 18%.",
            "sources": [{"document": "report.pdf", "page": 4}],
            "chunks": _chunks(),
        }
    )

    assert result["is_valid"] is True
    assert "Documento: report.pdf" in result["answer"]
    assert "Página: 4" in result["answer"]


def test_validate_answer_without_chunks() -> None:
    nodes = RAGNodes(retriever=MagicMock(), chain=MagicMock())
    result = nodes.validate_answer(
        {"answer": "Cualquier cosa inventada", "sources": [], "chunks": []}
    )

    assert result["answer"] == INSUFFICIENT_INFO_MESSAGE
    assert result["is_valid"] is True


def test_rag_graph_four_node_pipeline() -> None:
    retriever = MagicMock()
    retriever.retrieve_with_scores.return_value = _chunks()

    chain = MagicMock()
    chain.build_context.return_value = "contexto de prueba"
    chain.extract_sources.return_value = [
        {"document": "report.pdf", "page": 4, "rank": 1, "score": 0.15}
    ]
    chain.generate.return_value = "El margen operativo fue 18%."
    chain.attach_sources.side_effect = (
        lambda answer, sources: f"{answer}\n\n---\nFuentes:\n"
        f"- Documento: {sources[0]['document']} | Página: {sources[0]['page']}"
    )

    graph = RAGGraph(retriever=retriever, chain=chain)
    result = graph.invoke("¿Cuál es el margen operativo?")

    retriever.retrieve_with_scores.assert_called_once_with(
        "¿Cuál es el margen operativo?"
    )
    chain.generate.assert_called_once()
    assert result.cleaned_query == "¿Cuál es el margen operativo?"
    assert result.analysis["intent"] == "financial_lookup"
    assert result.is_valid is True
    assert "Documento: report.pdf" in result.answer
    assert result.sources[0]["page"] == 4


def test_rag_graph_rejects_empty_query() -> None:
    graph = RAGGraph(retriever=MagicMock(), chain=MagicMock())
    with pytest.raises(RAGError, match="Query cannot be empty"):
        graph.invoke("  ")
