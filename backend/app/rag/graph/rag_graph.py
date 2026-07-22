"""Grafo LangGraph del pipeline RAG."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph

from backend.app.core.exceptions import RAGError, RetrievalError
from backend.app.rag.chains.rag_chain import RAGChain
from backend.app.rag.retriever.document_retriever import DocumentRetriever, RetrievedChunk


class RAGState(TypedDict, total=False):
    query: str
    chunks: List[RetrievedChunk]
    context: str
    answer: str
    sources: List[Dict[str, Any]]


@dataclass
class RAGResult:
    query: str
    answer: str
    context: str
    sources: List[Dict[str, Any]] = field(default_factory=list)
    chunks_used: int = 0


class RAGGraph:
    """
    Orquesta el flujo:

    Usuario → Retriever → Contexto → Prompt → GPT → Respuesta
    """

    def __init__(
        self,
        retriever: Optional[DocumentRetriever] = None,
        chain: Optional[RAGChain] = None,
    ) -> None:
        self.retriever = retriever or DocumentRetriever()
        self.chain = chain or RAGChain()
        self._graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(RAGState)
        graph.add_node("retrieve", self._retrieve_node)
        graph.add_node("build_context", self._build_context_node)
        graph.add_node("generate", self._generate_node)

        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "build_context")
        graph.add_edge("build_context", "generate")
        graph.add_edge("generate", END)

        return graph.compile()

    def _retrieve_node(self, state: RAGState) -> RAGState:
        chunks = self.retriever.retrieve_with_scores(state["query"])
        return {"chunks": chunks}

    def _build_context_node(self, state: RAGState) -> RAGState:
        chunks = state.get("chunks") or []
        context = self.chain.build_context(chunks)
        sources = self.chain.extract_sources(chunks)
        return {"context": context, "sources": sources}

    def _generate_node(self, state: RAGState) -> RAGState:
        raw_answer = self.chain.generate(
            question=state["query"],
            context=state.get("context") or "",
        )
        answer = self.chain.attach_sources(
            answer=raw_answer,
            sources=state.get("sources") or [],
        )
        return {"answer": answer}

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
        )
