"""Endpoints de carga de documentos."""

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.core.exceptions import InvalidDocumentError
from backend.app.models.schemas import UploadResponse
from backend.app.services.document_service import DocumentService

router = APIRouter(tags=["documents"])
document_service = DocumentService()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    try:
        saved_path = document_service.save_pdf(file)
    except InvalidDocumentError as exc:
        raise HTTPException(status_code=400, detail=exc.message) from exc

    return UploadResponse(
        filename=saved_path.name,
        path=str(saved_path),
        size_bytes=saved_path.stat().st_size,
    )
