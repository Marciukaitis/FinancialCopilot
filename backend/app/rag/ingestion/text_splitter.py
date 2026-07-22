"""División de documentos en chunks con RecursiveCharacterTextSplitter."""

from typing import List, Optional

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.app.config.settings import settings

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200


class DocumentChunker:
    """Divide documentos LangChain en chunks para indexación futura."""

    def __init__(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ) -> None:
        self.chunk_size = chunk_size if chunk_size is not None else settings.CHUNK_SIZE
        self.chunk_overlap = (
            chunk_overlap if chunk_overlap is not None else settings.CHUNK_OVERLAP
        )
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            add_start_index=True,
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Divide una lista de documentos en chunks."""
        if not documents:
            return []

        chunks = self._splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index

        return chunks

    def print_chunks(self, chunks: List[Document]) -> None:
        """Imprime los chunks por consola para verificación."""
        print(f"\nTotal chunks: {len(chunks)}")
        print(f"chunk_size={self.chunk_size} | chunk_overlap={self.chunk_overlap}\n")
        print("=" * 60)

        for chunk in chunks:
            filename = chunk.metadata.get("filename", "unknown")
            page = chunk.metadata.get("page", "n/a")
            index = chunk.metadata.get("chunk_index", "?")
            preview = chunk.page_content[:200].replace("\n", " ")

            print(f"[chunk {index}] file={filename} | page={page} | chars={len(chunk.page_content)}")
            print(preview)
            if len(chunk.page_content) > 200:
                print("...")
            print("-" * 60)
