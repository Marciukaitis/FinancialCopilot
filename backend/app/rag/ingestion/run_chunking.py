"""
Script de verificación: carga PDFs y muestra los chunks por consola.

Uso (desde la raíz del proyecto):
    python -m backend.app.rag.ingestion.run_chunking
"""

from backend.app.rag.ingestion.pdf_loader import PDFDocumentLoader
from backend.app.rag.ingestion.text_splitter import DocumentChunker


def main() -> None:
    loader = PDFDocumentLoader()
    documents = loader.load_documents()

    print(f"Documentos cargados: {len(documents)}")

    if not documents:
        print("No hay PDFs en data/documents. Subí uno con POST /upload y volvé a intentar.")
        return

    chunker = DocumentChunker()
    chunks = chunker.split_documents(documents)
    chunker.print_chunks(chunks)


if __name__ == "__main__":
    main()
