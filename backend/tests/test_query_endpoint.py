"""Tests del endpoint POST /query con memoria conversacional."""

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import backend.app.api.routes.queries as queries_module
from backend.app.main import app
from backend.app.rag.graph.state import RAGResult
from backend.app.services.query_service import QueryService

client = TestClient(app)


@pytest.fixture
def mock_query_service(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    service = MagicMock(spec=QueryService)
    service.ask.return_value = RAGResult(
        query="¿Y cuál es el plazo?",
        answer=(
            "El plazo máximo es 36 meses.\n\n"
            "---\nFuentes:\n- Documento: credito.pdf | Página: 5"
        ),
        context="contexto",
        thread_id="thread-123",
        sources=[
            {
                "document": "credito.pdf",
                "page": 5,
                "rank": 1,
                "score": 0.15,
            }
        ],
        chunks_used=1,
        cleaned_query="¿Y cuál es el plazo?",
        search_query="¿Cuál es el plazo máximo del crédito?",
        analysis={"intent": "financial_lookup", "is_followup": True},
        is_valid=True,
        validation_notes=["Validación OK: respuesta con documento y página."],
        conversation_history=[
            {"role": "user", "content": "¿Cuál es el monto máximo?"},
            {"role": "assistant", "content": "El monto máximo es 50000 USD."},
            {"role": "user", "content": "¿Y cuál es el plazo?"},
            {"role": "assistant", "content": "El plazo máximo es 36 meses."},
        ],
    )
    monkeypatch.setattr(queries_module, "query_service", service)
    return service


def test_query_endpoint_accepts_thread_id(mock_query_service: MagicMock) -> None:
    response = client.post(
        "/query",
        json={"query": "¿Y cuál es el plazo?", "thread_id": "thread-123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["thread_id"] == "thread-123"
    assert data["search_query"] == "¿Cuál es el plazo máximo del crédito?"
    assert data["analysis"]["is_followup"] is True
    assert data["sources"][0]["document"] == "credito.pdf"
    mock_query_service.ask.assert_called_once_with(
        "¿Y cuál es el plazo?",
        thread_id="thread-123",
    )
