"""Schemas Pydantic compartidos entre endpoints."""

from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    path: str
    size_bytes: int
    message: str = "Document uploaded successfully"
