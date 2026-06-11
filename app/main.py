from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config import get_settings
from app.database import close_database_connection, close_redis_connection

settings = get_settings()


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown lifecycle."""

    yield

    await close_redis_connection()
    await close_database_connection()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    application = FastAPI(
        title=settings.app_name,
        description=(
            "REST API for sports data collection, statistical odds calculation, "
            "and AI-assisted betting analysis."
        ),
        version=settings.app_version,
        debug=settings.app_debug,
        lifespan=lifespan,
    )

    application.include_router(api_router, prefix=settings.api_v1_prefix)

    @application.get("/", tags=["Root"])
    async def read_root() -> dict[str, str]:
        return {
            "name": settings.app_name,
            "environment": settings.app_env,
            "version": settings.app_version,
            "status": "running",
        }

    return application


app = create_app()