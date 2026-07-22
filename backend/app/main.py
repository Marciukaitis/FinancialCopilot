"""Punto de entrada de la aplicación FastAPI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import documents, health, queries, root
from backend.app.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación."""
    yield


def create_app() -> FastAPI:
    """Factory para crear y configurar la instancia de FastAPI."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="Consulta inteligente sobre documentación financiera con RAG.",
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(root.router)
    app.include_router(health.router)
    app.include_router(documents.router)
    app.include_router(queries.router)

    return app


app = create_app()
