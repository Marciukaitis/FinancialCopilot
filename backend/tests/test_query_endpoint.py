"""Tests del endpoint POST /query."""

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import backend.app.api.routes.queries as queries_module
from backend.app.main import app
from backend.app.rag.graph.rag_graph import RAGResult
from backend.app.services.query_service import QueryService

client = TestClient(app)


@pytest.fixture
def mock_query_service(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    service = MagicMock(spec=QueryService)
    service.ask.return_value = RAGResult(
        query="¿Cuál es el margen operativo?",
        answer="El margen operativo fue 18%.",
        context="contexto",
        sources=[
            {
                "filename": "report.pdf",
                "page": 3,
                "rank": 1,
                "score": 0.15,
            }
        ],
        chunks_used=2,
    )
    monkeypatch.setattr(queries_module, "query_service", service)
    return service


def test_query_endpoint(mock_query_service: MagicMock) -> None:
    response = client.post(
        "/query",
        json={"query": "¿Cuál es el margen operativo?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "El margen operativo fue 18%."
    assert data["chunks_used"] == 2
    assert data["sources"][0]["filename"] == "report.pdf"
    mock_query_service.ask.assert_called_once_with("¿Cuál es el margen operativo?")
