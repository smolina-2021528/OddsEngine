from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import check_database_connection, check_redis_connection
from app.schemas.health import ComponentHealth, HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse | JSONResponse:
    """Return application and dependency health status."""

    settings = get_settings()

    database_is_available = await check_database_connection()
    redis_is_available = await check_redis_connection()

    response = HealthResponse(
        status="ok" if database_is_available and redis_is_available else "degraded",
        application=ComponentHealth(
            status="ok",
            detail=f"{settings.app_name} is running in {settings.app_env} mode.",
        ),
        database=ComponentHealth(
            status="ok" if database_is_available else "error",
            detail=(
                "PostgreSQL connection is available."
                if database_is_available
                else "PostgreSQL connection is not available."
            ),
        ),
        redis=ComponentHealth(
            status="ok" if redis_is_available else "error",
            detail=(
                "Redis connection is available."
                if redis_is_available
                else "Redis connection is not available."
            ),
        ),
    )

    if response.status == "ok":
        return response

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=response.model_dump(),
    )