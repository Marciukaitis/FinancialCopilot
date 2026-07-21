"""Tests de los endpoints raíz y de salud."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Finance Copilot API running"


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
