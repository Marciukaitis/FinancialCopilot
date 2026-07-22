"""Servicio de carga y almacenamiento de documentos PDF."""

from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import UploadFile

from backend.app.config.settings import settings
from backend.app.core.exceptions import InvalidDocumentError

PDF_MAGIC_BYTES = b"%PDF"
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/x-pdf",
    "application/acrobat",
    "applications/vnd.pdf",
    "text/pdf",
    "application/octet-stream",
}


class DocumentService:
    """Gestiona la validación y persistencia de archivos PDF."""

    def __init__(self, documents_directory: Optional[str] = None) -> None:
        self.documents_directory = Path(
            documents_directory or settings.DOCUMENTS_DIRECTORY
        )

    def save_pdf(self, file: UploadFile) -> Path:
        """Valida y guarda un archivo PDF en el directorio configurado."""
        self._validate_pdf(file)

        self.documents_directory.mkdir(parents=True, exist_ok=True)

        destination = self._resolve_destination_path(file.filename)
        content = file.file.read()

        if not content.startswith(PDF_MAGIC_BYTES):
            raise InvalidDocumentError("The file content is not a valid PDF.")

        destination.write_bytes(content)
        return destination

    def _validate_pdf(self, file: UploadFile) -> None:
        if not file.filename:
            raise InvalidDocumentError("Filename is required.")

        if Path(file.filename).suffix.lower() != ".pdf":
            raise InvalidDocumentError("Only PDF files are allowed.")

        if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
            raise InvalidDocumentError("Invalid content type. Only PDF files are allowed.")

    def _resolve_destination_path(self, filename: str) -> Path:
        safe_name = Path(filename).name
        destination = self.documents_directory / safe_name

        if destination.exists():
            destination = self.documents_directory / f"{uuid4().hex}_{safe_name}"

        return destination
