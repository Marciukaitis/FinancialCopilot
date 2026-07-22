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

    assert "Documento: report.pdf" in context
    assert "Página: 4" in context  # page 3 (0-index) -> 4
    assert "Operating margin was 18%" in context


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_extract_sources_returns_document_and_page(mock_chat: MagicMock) -> None:
    chain = RAGChain(api_key="test-key")
    sources = chain.extract_sources(_chunks())

    assert len(sources) == 2
    assert sources[0]["document"] == "report.pdf"
    assert sources[0]["page"] == 4
    assert sources[1]["page"] == 2


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_attach_sources_appends_document_and_page(mock_chat: MagicMock) -> None:
    chain = RAGChain(api_key="test-key")
    sources = [{"document": "report.pdf", "page": 4}]
    answer = chain.attach_sources("El margen operativo fue 18%.", sources)

    assert "El margen operativo fue 18%." in answer
    assert "Documento: report.pdf" in answer
    assert "Página: 4" in answer


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_attach_sources_skips_when_insufficient_info(mock_chat: MagicMock) -> None:
    chain = RAGChain(api_key="test-key")
    sources = [{"document": "report.pdf", "page": 4}]
    message = (
        "No poseo suficiente información en los documentos disponibles "
        "para responder esta pregunta."
    )
    answer = chain.attach_sources(message, sources)
    assert answer == message
    assert "Fuentes:" not in answer


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_generate_uses_context_only_prompt(mock_chat: MagicMock) -> None:
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(content="El margen operativo fue 18%.")
    mock_chat.return_value = llm

    chain = RAGChain(api_key="test-key")
    answer = chain.generate(
        question="¿Cuál es el margen operativo?",
        context="[Documento: report.pdf | Página: 4]\nOperating margin was 18%.",
    )

    assert answer == "El margen operativo fue 18%."
    messages = llm.invoke.call_args[0][0]
    serialized = " ".join(str(message.content) for message in messages)
    assert "cita siempre la fuente" in serialized.lower()
    assert "español" in serialized.lower()


def test_rag_chain_requires_api_key() -> None:
    with pytest.raises(RAGError, match="OPENAI_API_KEY"):
        RAGChain(api_key="")


def test_rag_graph_pipeline_includes_sources_in_answer() -> None:
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

    chain.attach_sources.assert_called_once()
    assert "Documento: report.pdf" in result.answer
    assert "Página: 4" in result.answer
    assert result.sources[0]["document"] == "report.pdf"
    assert result.sources[0]["page"] == 4


def test_rag_graph_rejects_empty_query() -> None:
    graph = RAGGraph(retriever=MagicMock(), chain=MagicMock())
    with pytest.raises(RAGError, match="Query cannot be empty"):
        graph.invoke("  ")
