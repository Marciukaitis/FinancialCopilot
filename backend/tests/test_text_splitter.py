"""Tests del DocumentChunker."""

from langchain_core.documents import Document

from backend.app.rag.ingestion.text_splitter import DocumentChunker


def test_split_empty_list() -> None:
    chunker = DocumentChunker()
    assert chunker.split_documents([]) == []


def test_split_respects_chunk_size() -> None:
    # Texto largo: más de 1000 caracteres para forzar varios chunks
    long_text = ("Finance report section. " * 80).strip()
    documents = [
        Document(
            page_content=long_text,
            metadata={"filename": "report.pdf", "source": "data/documents/report.pdf"},
        )
    ]

    chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
    chunks = chunker.split_documents(documents)

    assert len(chunks) > 1
    assert all(len(chunk.page_content) <= 1000 for chunk in chunks)
    assert all("chunk_index" in chunk.metadata for chunk in chunks)
    assert chunks[0].metadata["filename"] == "report.pdf"


def test_print_chunks_does_not_raise(capsys) -> None:
    documents = [
        Document(
            page_content="Short financial summary for testing.",
            metadata={"filename": "summary.pdf", "page": 0},
        )
    ]
    chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
    chunks = chunker.split_documents(documents)
    chunker.print_chunks(chunks)

    captured = capsys.readouterr()
    assert "Total chunks:" in captured.out
    assert "summary.pdf" in captured.out
