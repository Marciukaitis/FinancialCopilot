"""
Script de verificación: carga PDFs, hace chunking y genera embeddings locales.

Uso (desde la raíz del proyecto):
    python -m backend.app.rag.embeddings.run_embeddings
"""

from backend.app.rag.embeddings.huggingface_embeddings import EmbeddingService
from backend.app.rag.ingestion.pdf_loader import PDFDocumentLoader
from backend.app.rag.ingestion.text_splitter import DocumentChunker


def main() -> None:
    documents = PDFDocumentLoader().load_documents()
    print(f"Documentos cargados: {len(documents)}")

    if not documents:
        print("No hay PDFs en data/documents. Subí uno con POST /upload y volvé a intentar.")
        return

    chunks = DocumentChunker().split_documents(documents)
    print(f"Chunks generados: {len(chunks)}")

    service = EmbeddingService()
    embedded = service.embed_chunks(chunks)
    service.print_embeddings(embedded)


if __name__ == "__main__":
    main()
