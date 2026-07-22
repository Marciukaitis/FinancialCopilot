"""Carga de documentos PDF con LangChain."""

from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_core.documents import Document

from backend.app.config.settings import settings
from backend.app.core.exceptions import PDFLoadError


class PDFDocumentLoader:
    """Recorre data/documents y carga todos los PDFs como documentos LangChain."""

    def __init__(self, documents_directory: Optional[str] = None) -> None:
        self.documents_directory = Path(
            documents_directory or settings.DOCUMENTS_DIRECTORY
        )

    def load_documents(self) -> List[Document]:
        """
        Recorre la carpeta de documentos, lee todos los PDFs
        y devuelve una lista de Document de LangChain.
        """
        if not self.documents_directory.exists():
            return []

        if not any(self.documents_directory.glob("*.pdf")):
            return []

        try:
            loader = DirectoryLoader(
                str(self.documents_directory),
                glob="*.pdf",
                loader_cls=PyPDFLoader,
                show_progress=False,
            )
            documents = loader.load()
        except Exception as exc:
            raise PDFLoadError(
                "Failed to load PDFs from documents directory",
                filepath=str(self.documents_directory),
            ) from exc

        for document in documents:
            source_path = Path(document.metadata.get("source", ""))
            document.metadata["filename"] = source_path.name

        return documents
