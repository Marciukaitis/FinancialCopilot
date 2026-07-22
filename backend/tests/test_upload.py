"""Tests del endpoint de carga de documentos."""

import io
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import backend.app.api.routes.documents as documents_module
from backend.app.main import app
from backend.app.services.document_service import DocumentService
from backend.app.services.indexing_service import IndexingResult

client = TestClient(app)

MINIMAL_PDF = b"""%PDF-1.4
1 0 obj<<>>endobj
trailer<<>>
%%EOF
"""


@pytest.fixture
def documents_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    upload_dir = tmp_path / "documents"
    monkeypatch.setattr(
        documents_module,
        "document_service",
        DocumentService(documents_directory=str(upload_dir)),
    )

    indexing = MagicMock()
    indexing.reindex_all.return_value = IndexingResult(
        documents_loaded=1,
        chunks_indexed=2,
        collection_name="finance_documents",
        total_in_store=2,
    )
    monkeypatch.setattr(documents_module, "indexing_service", indexing)
    return upload_dir


def test_upload_pdf(documents_dir: Path) -> None:
    response = client.post(
        "/upload",
        files={"file": ("report.pdf", io.BytesIO(MINIMAL_PDF), "application/pdf")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "report.pdf"
    assert data["size_bytes"] > 0
    assert data["message"] == "Document uploaded successfully"
    assert data["chunks_indexed"] == 2
    assert data["collection_name"] == "finance_documents"
    assert (documents_dir / "report.pdf").exists()


def test_upload_rejects_non_pdf() -> None:
    response = client.post(
        "/upload",
        files={"file": ("notes.txt", io.BytesIO(b"hello"), "text/plain")},
    )

    assert response.status_code == 400
    assert "Only PDF files are allowed" in response.json()["detail"]


def test_upload_rejects_invalid_pdf_content(documents_dir: Path) -> None:
    response = client.post(
        "/upload",
        files={"file": ("fake.pdf", io.BytesIO(b"not a pdf"), "application/pdf")},
    )

    assert response.status_code == 400
    assert "not a valid PDF" in response.json()["detail"]


def test_reindex_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    indexing = MagicMock()
    indexing.reindex_all.return_value = IndexingResult(
        documents_loaded=3,
        chunks_indexed=10,
        collection_name="finance_documents",
        total_in_store=10,
    )
    monkeypatch.setattr(documents_module, "indexing_service", indexing)

    response = client.post("/reindex")

    assert response.status_code == 200
    data = response.json()
    assert data["documents_loaded"] == 3
    assert data["chunks_indexed"] == 10
    assert data["collection_name"] == "finance_documents"
    assert data["total_in_store"] == 10
