"""Tests del PDF Loader con LangChain."""

from pathlib import Path

from pypdf import PdfWriter

from backend.app.rag.ingestion.pdf_loader import PDFDocumentLoader


def _create_pdf(path: Path, text: str = "Finance report content") -> None:
    """Crea un PDF mínimo válido para tests."""
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    # pypdf blank pages have no text; content validation is structural
    with path.open("wb") as file:
        writer.write(file)


def test_load_documents_returns_empty_when_directory_missing(tmp_path: Path) -> None:
    loader = PDFDocumentLoader(documents_directory=str(tmp_path / "missing"))
    assert loader.load_documents() == []


def test_load_documents_returns_empty_when_no_pdfs(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("not a pdf")
    loader = PDFDocumentLoader(documents_directory=str(tmp_path))
    assert loader.load_documents() == []


def test_load_documents_reads_all_pdfs(tmp_path: Path) -> None:
    _create_pdf(tmp_path / "report_a.pdf")
    _create_pdf(tmp_path / "report_b.pdf")
    (tmp_path / "ignore.txt").write_text("skip me")

    loader = PDFDocumentLoader(documents_directory=str(tmp_path))
    documents = loader.load_documents()

    assert len(documents) >= 2
    filenames = {doc.metadata.get("filename") for doc in documents}
    assert "report_a.pdf" in filenames
    assert "report_b.pdf" in filenames
    assert all("source" in doc.metadata for doc in documents)
