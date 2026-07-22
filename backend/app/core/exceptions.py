"""Excepciones personalizadas de la aplicación."""


class InvalidDocumentError(Exception):
    """Error de validación al procesar un documento."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class PDFLoadError(Exception):
    """Error al cargar un documento PDF."""

    def __init__(self, message: str, filepath: str) -> None:
        self.message = message
        self.filepath = filepath
        super().__init__(message)


class EmbeddingError(Exception):
    """Error al generar embeddings."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class VectorStoreError(Exception):
    """Error al operar sobre la base vectorial."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class RetrievalError(Exception):
    """Error al recuperar documentos desde el vector store."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
