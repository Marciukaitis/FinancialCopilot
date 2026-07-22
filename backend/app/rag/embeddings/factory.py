"""Factory de embeddings locales con HuggingFace / Sentence Transformers."""

from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings

from backend.app.config.settings import settings
from backend.app.core.exceptions import EmbeddingError


def build_embeddings(model_name: Optional[str] = None) -> HuggingFaceEmbeddings:
    """Crea la función de embeddings local."""
    model = model_name or settings.EMBEDDING_MODEL

    try:
        return HuggingFaceEmbeddings(
            model_name=model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    except Exception as exc:
        raise EmbeddingError(
            f"Failed to load HuggingFace embeddings '{model}': {exc}"
        ) from exc
