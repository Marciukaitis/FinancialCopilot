"""Grafo LangGraph del pipeline RAG con StateGraph."""

from typing import Optional

from langgraph.graph import END, StateGraph

from backend.app.core.exceptions import RAGError, RetrievalError
from backend.app.rag.chains.rag_chain import RAGChain
from backend.app.rag.graph.nodes import RAGNodes
from backend.app.rag.graph.state import RAGResult, RAGState
from backend.app.rag.retriever.document_retriever import DocumentRetriever


class RAGGraph:
    """
    Flujo LangGraph:

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
    ) -> None:
        self.retriever = retriever or DocumentRetriever()
        self.chain = chain or RAGChain()
        self.nodes = RAGNodes(retriever=self.retriever, chain=self.chain)
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

        return graph.compile()

    def invoke(self, query: str) -> RAGResult:
        query = (query or "").strip()
        if not query:
            raise RAGError("Query cannot be empty.")

        try:
            final_state = self._graph.invoke({"query": query})
        except RetrievalError:
            raise
        except RAGError:
            raise
        except Exception as exc:
            raise RAGError(f"RAG pipeline failed: {exc}") from exc

        chunks = final_state.get("chunks") or []
        return RAGResult(
            query=query,
            answer=final_state.get("answer") or "",
            context=final_state.get("context") or "",
            sources=final_state.get("sources") or [],
            chunks_used=len(chunks),
            cleaned_query=final_state.get("cleaned_query") or query,
            analysis=final_state.get("analysis") or {},
            is_valid=bool(final_state.get("is_valid", True)),
            validation_notes=final_state.get("validation_notes") or [],
        )
