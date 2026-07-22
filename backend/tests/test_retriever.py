"""Tests del DocumentRetriever (sin modelo real)."""

from typing import List
from unittest.mock import MagicMock

import pytest
from langchain_core.documents import Document

from backend.app.core.exceptions import RetrievalError
from backend.app.rag.retriever.document_retriever import DocumentRetriever


def _docs() -> List[Document]:
    return [
        Document(page_content="Revenue grew 10%.", metadata={"filename": "a.pdf"}),
        Document(page_content="Operating margin improved.", metadata={"filename": "b.pdf"}),
        Document(page_content="Cash flow remained stable.", metadata={"filename": "c.pdf"}),
        Document(page_content="Debt ratio decreased.", metadata={"filename": "d.pdf"}),
    ]


def test_retrieve_uses_k_four() -> None:
    vector_store = MagicMock()
    langchain_store = MagicMock()
    retriever_mock = MagicMock()
    retriever_mock.invoke.return_value = _docs()
    langchain_store.as_retriever.return_value = retriever_mock
    vector_store.get_vectorstore.return_value = langchain_store
    vector_store.collection_name = "finance_documents"

    retriever = DocumentRetriever(vector_store=vector_store, k=4)
    results = retriever.retrieve("margen operativo")

    langchain_store.as_retriever.assert_called_once_with(search_kwargs={"k": 4})
    assert len(results) == 4
    assert results[0].metadata["filename"] == "a.pdf"


def test_retrieve_with_scores() -> None:
    vector_store = MagicMock()
    langchain_store = MagicMock()
    langchain_store.as_retriever.return_value = MagicMock()
    langchain_store.similarity_search_with_score.return_value = [
        (_docs()[0], 0.12),
        (_docs()[1], 0.25),
    ]
    vector_store.get_vectorstore.return_value = langchain_store
    vector_store.collection_name = "finance_documents"

    retriever = DocumentRetriever(vector_store=vector_store, k=4)
    results = retriever.retrieve_with_scores("margen")

    assert len(results) == 2
    assert results[0].rank == 1
    assert results[0].score == 0.12
    assert results[0].source == "a.pdf"
    langchain_store.similarity_search_with_score.assert_called_once_with(
        "margen",
        k=4,
    )


def test_retrieve_rejects_empty_query() -> None:
    vector_store = MagicMock()
    langchain_store = MagicMock()
    langchain_store.as_retriever.return_value = MagicMock()
    vector_store.get_vectorstore.return_value = langchain_store

    retriever = DocumentRetriever(vector_store=vector_store, k=4)

    with pytest.raises(RetrievalError, match="Query cannot be empty"):
        retriever.retrieve("   ")


def test_print_results(capsys) -> None:
    vector_store = MagicMock()
    langchain_store = MagicMock()
    langchain_store.as_retriever.return_value = MagicMock()
    vector_store.get_vectorstore.return_value = langchain_store
    vector_store.collection_name = "finance_documents"

    retriever = DocumentRetriever(vector_store=vector_store, k=4)
    chunks = [
        type(
            "R",
            (),
            {
                "rank": 1,
                "source": "a.pdf",
                "score": 0.1,
                "content": "Revenue grew 10%.",
            },
        )()
    ]
    # Use real RetrievedChunk via retrieve_with_scores mock path
    langchain_store.similarity_search_with_score.return_value = [(_docs()[0], 0.1)]
    results = retriever.retrieve_with_scores("revenue")
    retriever.print_results("revenue", results)

    output = capsys.readouterr().out
    assert "Query: revenue" in output
    assert "k=4" in output
    assert "a.pdf" in output
