# """Generación de embeddings con OpenAI (sin persistencia en vector store)."""

# from dataclasses import dataclass
# from typing import List, Optional

# from langchain_core.documents import Document
# from langchain_openai import OpenAIEmbeddings

# from backend.app.config.settings import settings
# from backend.app.core.exceptions import EmbeddingError


# @dataclass
# class EmbeddedChunk:
#     """Chunk con su vector de embedding asociado."""

#     document: Document
#     embedding: List[float]
#     index: int

#     @property
#     def dimensions(self) -> int:
#         return len(self.embedding)

#     @property
#     def content(self) -> str:
#         return self.document.page_content

#     @property
#     def metadata(self) -> dict:
#         return self.document.metadata


# class EmbeddingService:
#     """Convierte chunks de texto en embeddings con OpenAIEmbeddings."""

#     def __init__(
#         self,
#         api_key: Optional[str] = None,
#         model: Optional[str] = None,
#     ) -> None:
#         self.api_key = api_key or settings.OPENAI_API_KEY
#         self.model = model or settings.EMBEDDING_MODEL

#         if not self.api_key:
#             raise EmbeddingError(
#                 "OPENAI_API_KEY is required to generate embeddings."
#             )

#         self._embeddings = OpenAIEmbeddings(
#             model=self.model,
#             api_key=self.api_key,
#         )

#     def embed_chunks(self, chunks: List[Document]) -> List[EmbeddedChunk]:
#         """Genera un embedding por cada chunk."""
#         if not chunks:
#             return []

#         texts = [chunk.page_content for chunk in chunks]

#         try:
#             vectors = self._embeddings.embed_documents(texts)
#         except Exception as exc:
#             raise EmbeddingError(f"Failed to generate embeddings: {exc}") from exc

#         if len(vectors) != len(chunks):
#             raise EmbeddingError(
#                 "Mismatch between number of chunks and embeddings returned."
#             )

#         return [
#             EmbeddedChunk(document=chunk, embedding=vector, index=index)
#             for index, (chunk, vector) in enumerate(zip(chunks, vectors))
#         ]

#     def print_embeddings(self, embedded_chunks: List[EmbeddedChunk]) -> None:
#         """Imprime un resumen de los embeddings por consola."""
#         print(f"\nTotal embeddings: {len(embedded_chunks)}")
#         print(f"model={self.model}\n")
#         print("=" * 60)

#         for item in embedded_chunks:
#             filename = item.metadata.get("filename", "unknown")
#             preview = item.content[:120].replace("\n", " ")
#             print(
#                 f"[embedding {item.index}] "
#                 f"file={filename} | dims={item.dimensions} | chars={len(item.content)}"
#             )
#             print(f"preview: {preview}")
#             print(f"vector[:5]: {item.embedding[:5]}")
#             print("-" * 60)
