"""Tests del pipeline RAG con LangGraph + memoria conversacional."""

from typing import List
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document
from langgraph.checkpoint.memory import MemorySaver

from backend.app.core.exceptions import RAGError
from backend.app.rag.chains.rag_chain import RAGChain
from backend.app.rag.graph.nodes import INSUFFICIENT_INFO_MESSAGE, RAGNodes
from backend.app.rag.graph.rag_graph import RAGGraph
from backend.app.rag.retriever.document_retriever import RetrievedChunk


def _chunks() -> List[RetrievedChunk]:
    return [
        RetrievedChunk(
            document=Document(
                page_content="El monto máximo es 50000 USD.",
                metadata={"filename": "credito.pdf", "page": 2},
            ),
            score=0.15,
            rank=1,
        ),
        RetrievedChunk(
            document=Document(
                page_content="El plazo máximo es 36 meses.",
                metadata={"filename": "credito.pdf", "page": 4},
            ),
            score=0.22,
            rank=2,
        ),
    ]


@patch("backend.app.rag.chains.rag_chain.ChatOpenAI")
def test_generate_includes_chat_history(mock_chat: MagicMock) -> None:
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(content="El plazo es 36 meses.")
    mock_chat.return_value = llm

    chain = RAGChain(api_key="test-key")
    chain.generate(
        question="¿Y cuál es el plazo?",
        context="[Documento: credito.pdf | Página: 5]\nEl plazo máximo es 36 meses.",
        chat_history=[
            {"role": "user", "content": "¿Cuál es el monto máximo?"},
            {"role": "assistant", "content": "El monto máximo es 50000 USD."},
        ],
    )

    messages = llm.invoke.call_args[0][0]
    serialized = " ".join(str(message.content) for message in messages)
    assert "monto máximo" in serialized.lower()
    assert "historial" in serialized.lower()


def test_is_followup_detection() -> None:
    history = [
        {"role": "user", "content": "¿Cuál es el monto máximo?"},
        {"role": "assistant", "content": "El monto máximo es 50000 USD."},
    ]
    assert RAGNodes._is_followup("¿Y cuál es el plazo?", history) is True
    assert RAGNodes._is_followup("¿Cuál es el monto máximo del crédito hipotecario?", []) is False


def test_analyze_question_rewrites_followup() -> None:
    chain = MagicMock()
    chain.rewrite_followup_query.return_value = "¿Cuál es el plazo máximo del crédito?"
    nodes = RAGNodes(retriever=MagicMock(), chain=chain)

    result = nodes.analyze_question(
        {
            "query": "¿Y cuál es el plazo?",
            "conversation_history": [
                {"role": "user", "content": "¿Cuál es el monto máximo?"},
                {"role": "assistant", "content": "El monto máximo es 50000 USD."},
            ],
        }
    )

    assert result["analysis"]["is_followup"] is True
    assert result["search_query"] == "¿Cuál es el plazo máximo del crédito?"
    chain.rewrite_followup_query.assert_called_once()


def test_validate_answer_appends_conversation_history() -> None:
    chain = MagicMock()
    chain.attach_sources.side_effect = lambda answer, sources: (
        f"{answer}\n\n---\nFuentes:\n"
        f"- Documento: {sources[0]['document']} | Página: {sources[0]['page']}"
    )
    nodes = RAGNodes(retriever=MagicMock(), chain=chain)

    result = nodes.validate_answer(
        {
            "query": "¿Cuál es el monto máximo?",
            "cleaned_query": "¿Cuál es el monto máximo?",
            "answer": "El monto máximo es 50000 USD.",
            "sources": [{"document": "credito.pdf", "page": 3}],
            "chunks": _chunks(),
        }
    )

    assert len(result["conversation_history"]) == 2
    assert result["conversation_history"][0]["role"] == "user"
    assert result["conversation_history"][1]["role"] == "assistant"


def test_rag_graph_memory_across_turns() -> None:
    retriever = MagicMock()
    retriever.retrieve_with_scores.side_effect = [
        [_chunks()[0]],
        [_chunks()[1]],
    ]

    chain = MagicMock()
    chain.build_context.side_effect = [
        "contexto monto",
        "contexto plazo",
    ]
    chain.extract_sources.side_effect = [
        [{"document": "credito.pdf", "page": 3, "rank": 1, "score": 0.1}],
        [{"document": "credito.pdf", "page": 5, "rank": 1, "score": 0.2}],
    ]
    chain.rewrite_followup_query.return_value = "¿Cuál es el plazo máximo del crédito?"
    chain.generate.side_effect = [
        "El monto máximo es 50000 USD.",
        "El plazo máximo es 36 meses.",
    ]
    chain.attach_sources.side_effect = (
        lambda answer, sources: f"{answer}\n\n---\nFuentes:\n"
        f"- Documento: {sources[0]['document']} | Página: {sources[0]['page']}"
    )

    graph = RAGGraph(
        retriever=retriever,
        chain=chain,
        checkpointer=MemorySaver(),
    )

    first = graph.invoke("¿Cuál es el monto máximo?", thread_id="demo-thread")
    second = graph.invoke("¿Y cuál es el plazo?", thread_id="demo-thread")

    assert first.thread_id == "demo-thread"
    assert second.thread_id == "demo-thread"
    assert second.analysis["is_followup"] is True
    assert len(second.conversation_history) >= 4
    assert "plazo" in second.answer.lower()
    chain.rewrite_followup_query.assert_called()


def test_rag_graph_rejects_empty_query() -> None:
    graph = RAGGraph(
        retriever=MagicMock(),
        chain=MagicMock(),
        checkpointer=MemorySaver(),
    )
    with pytest.raises(RAGError, match="Query cannot be empty"):
        graph.invoke("  ")


def test_validate_answer_without_chunks() -> None:
    nodes = RAGNodes(retriever=MagicMock(), chain=MagicMock())
    result = nodes.validate_answer(
        {
            "query": "hola",
            "cleaned_query": "hola",
            "answer": "inventado",
            "sources": [],
            "chunks": [],
        }
    )
    assert result["answer"] == INSUFFICIENT_INFO_MESSAGE
