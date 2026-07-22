"""Grafo LangGraph del pipeline RAG con StateGraph y MemorySaver."""

from typing import Optional
from uuid import uuid4

from langgraph.graph import END, StateGraph

from backend.app.core.exceptions import RAGError, RetrievalError
from backend.app.rag.chains.rag_chain import RAGChain
from backend.app.rag.graph.memory import memory_saver
from backend.app.rag.graph.nodes import RAGNodes
from backend.app.rag.graph.state import RAGResult, RAGState
from backend.app.rag.retriever.document_retriever import DocumentRetriever

class RAGGraph:
    """
    Flujo LangGraph con memoria conversacional:

    Usuario
      → analyze_question
      → search_documents
      → generate_answer
      → validate_answer
      → Usuario
    """

    def __init__(
        self,
        retriever: Optional[DocumentRetriever] = None,
        chain: Optional[RAGChain] = None,
        checkpointer=None,
    ) -> None:
        self.retriever = retriever or DocumentRetriever()
        self.chain = chain or RAGChain()
        self.nodes = RAGNodes(retriever=self.retriever, chain=self.chain)
        self.checkpointer = checkpointer if checkpointer is not None else memory_saver
        self._graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(RAGState)

        graph.add_node("analyze_question", self.nodes.analyze_question)
        graph.add_node("search_documents", self.nodes.search_documents)
        graph.add_node("generate_answer", self.nodes.generate_answer)
        graph.add_node("validate_answer", self.nodes.validate_answer)

        graph.set_entry_point("analyze_question")
        graph.add_edge("analyze_question", "search_documents")
        graph.add_edge("search_documents", "generate_answer")
        graph.add_edge("generate_answer", "validate_answer")
        graph.add_edge("validate_answer", END)

        return graph.compile(checkpointer=self.checkpointer)

    def invoke(self, query: str, thread_id: Optional[str] = None) -> RAGResult:
        query = (query or "").strip()
        if not query:
            raise RAGError("Query cannot be empty.")

        thread_id = (thread_id or "").strip() or str(uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        try:
            final_state = self._graph.invoke({"query": query}, config=config)
        except RetrievalError:
            raise
        except RAGError:
            raise
        except Exception as exc:
            raise RAGError(f"RAG pipeline failed: {exc}") from exc

        chunks = final_state.get("chunks") or []
        retrieved_chunks = [
            {
                "rank": chunk.rank,
                "content": chunk.content,
                "source": RAGChain.normalize_document_name(chunk.source),
                "score": _similarity_score(chunk.score),
                "metadata": {
                    **(chunk.metadata or {}),
                    "page": _readable_page(chunk.metadata),
                    "distance": chunk.score,
                },
            }
            for chunk in chunks
        ]
        return RAGResult(
            query=query,
            answer=final_state.get("answer") or "",
            context=final_state.get("context") or "",
            thread_id=thread_id,
            sources=final_state.get("sources") or [],
            retrieved_chunks=retrieved_chunks,
            chunks_used=len(chunks),
            cleaned_query=final_state.get("cleaned_query") or query,
            search_query=final_state.get("search_query") or query,
            analysis=final_state.get("analysis") or {},
            is_valid=bool(final_state.get("is_valid", True)),
            validation_notes=final_state.get("validation_notes") or [],
            conversation_history=final_state.get("conversation_history") or [],
        )


def _similarity_score(distance: Optional[float]) -> Optional[float]:
    """Convierte distancia Chroma (menor = mejor) a similitud 0–1 para la UI."""
    if distance is None:
        return None
    try:
        return round(1.0 / (1.0 + float(distance)), 4)
    except (TypeError, ValueError):
        return None


def _readable_page(metadata: Optional[dict]) -> Optional[int]:
    if not metadata:
        return None
    page = metadata.get("page")
    if page is None or page == "n/a":
        return None
    try:
        page_number = int(page)
    except (TypeError, ValueError):
        return None
    return page_number + 1 if page_number >= 0 else page_number
