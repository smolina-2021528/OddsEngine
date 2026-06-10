from fastapi import FastAPI

from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "REST API for sports data collection, statistical odds calculation, "
        "and AI-assisted betting analysis."
    ),
    version=settings.app_version,
    debug=settings.app_debug,
)


@app.get("/", tags=["Root"])
async def read_root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "environment": settings.app_env,
        "version": settings.app_version,
        "status": "running",
    }