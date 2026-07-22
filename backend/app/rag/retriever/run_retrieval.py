"""
Script de verificación: búsqueda semántica en ChromaDB (sin LLM).

Uso (desde la raíz, con OPENAI_API_KEY y documentos indexados):
    python -m backend.app.rag.retriever.run_retrieval "¿cuál es el margen operativo?"
"""

import sys

from backend.app.rag.retriever.document_retriever import DocumentRetriever


def main() -> None:
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        query = input("Consulta: ").strip()

    if not query:
        print("Debés indicar una consulta.")
        sys.exit(1)

    retriever = DocumentRetriever()
    results = retriever.retrieve_with_scores(query)
    retriever.print_results(query, results)


if __name__ == "__main__":
    main()
