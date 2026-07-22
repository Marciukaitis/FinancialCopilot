"""
Script de verificación: reindexa todos los PDFs en ChromaDB.

Uso (desde la raíz del proyecto):
    python -m backend.app.rag.vectorstore.run_indexing
"""

from backend.app.services.indexing_service import IndexingService


def main() -> None:
    service = IndexingService()
    result = service.reindex_all()

    print("\nReindexación completada")
    print("=" * 60)
    print(f"Documentos cargados : {result.documents_loaded}")
    print(f"Chunks indexados    : {result.chunks_indexed}")
    print(f"Colección           : {result.collection_name}")
    print(f"Total en ChromaDB   : {result.total_in_store}")
    print("=" * 60)


if __name__ == "__main__":
    main()
