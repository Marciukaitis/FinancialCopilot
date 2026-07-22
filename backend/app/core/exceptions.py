"""Excepciones personalizadas de la aplicación."""


class InvalidDocumentError(Exception):
    """Error de validación al procesar un documento."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
