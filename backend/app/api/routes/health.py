"""Endpoints de salud y estado del servicio."""

from fastapi import APIRouter

from backend.app.config.settings import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
