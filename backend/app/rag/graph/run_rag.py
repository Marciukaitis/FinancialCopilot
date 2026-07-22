"""
Script de verificación del pipeline RAG con memoria conversacional.

Uso:
    python -m backend.app.rag.graph.run_rag
"""

import sys

from backend.app.rag.graph.rag_graph import RAGGraph


def main() -> None:
    graph = RAGGraph()
    thread_id = None

    print("Finance Copilot — chat con memoria (escribí 'salir' para terminar)")
    print("=" * 60)

    while True:
        if sys.argv[1:]:
            query = " ".join(sys.argv[1:]).strip()
            sys.argv = [sys.argv[0]]
        else:
            query = input("\nVos: ").strip()

        if not query:
            continue
        if query.lower() in {"salir", "exit", "quit"}:
            break

        result = graph.invoke(query, thread_id=thread_id)
        thread_id = result.thread_id

        print(f"\nthread_id: {result.thread_id}")
        print(f"follow-up: {result.analysis.get('is_followup')}")
        print(f"search_query: {result.search_query}")
        print("-" * 60)
        print("Copilot:")
        print(result.answer)
        print("-" * 60)
        for source in result.sources:
            page = source.get("page")
            page_label = str(page) if page is not None else "desconocida"
            print(f"  Fuente → Documento: {source.get('document')} | Página: {page_label}")


if __name__ == "__main__":
    main()
