"""Tests del endpoint de carga de documentos."""

import io
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import backend.app.api.routes.documents as documents_module
from backend.app.main import app
from backend.app.services.document_service import DocumentService

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
