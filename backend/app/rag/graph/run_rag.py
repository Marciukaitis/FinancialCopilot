"""
Script de verificación del pipeline RAG.

Uso (desde la raíz, con OPENAI_API_KEY y documentos indexados):
    python -m backend.app.rag.graph.run_rag "¿cuál es el margen operativo?"
"""

import sys

from backend.app.rag.graph.rag_graph import RAGGraph


def main() -> None:
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        query = input("Consulta: ").strip()

    if not query:
        print("Debés indicar una consulta.")
        sys.exit(1)

    result = RAGGraph().invoke(query)

    print("\n" + "=" * 60)
    print(f"Pregunta: {result.query}")
    print(f"Chunks usados: {result.chunks_used}")
    print("-" * 60)
    print("Respuesta:")
    print(result.answer)
    print("-" * 60)
    print("Fuentes:")
    if not result.sources:
        print("  (sin fuentes)")
    for source in result.sources:
        print(
            f"  - {source.get('filename')} "
            f"| page={source.get('page')} "
            f"| rank={source.get('rank')}"
        )
    print("=" * 60)


if __name__ == "__main__":
    main()
