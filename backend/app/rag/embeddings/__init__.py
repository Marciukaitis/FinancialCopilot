"""Módulo de embeddings locales."""

from backend.app.rag.embeddings.huggingface_embeddings import EmbeddedChunk, EmbeddingService

__all__ = ["EmbeddedChunk", "EmbeddingService"]
