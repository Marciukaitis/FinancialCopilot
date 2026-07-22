"""Cadenas LangChain para recuperación y generación."""

from backend.app.rag.chains.prompts import build_rag_prompt
from backend.app.rag.chains.rag_chain import RAGChain

__all__ = ["RAGChain", "build_rag_prompt"]
