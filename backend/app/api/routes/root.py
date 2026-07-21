"""Endpoint raíz de la API."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["root"])


@router.get("/", response_class=PlainTextResponse)
async def root() -> str:
    return "Finance Copilot API running"
