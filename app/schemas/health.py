from typing import Literal

from pydantic import BaseModel, Field


class ComponentHealth(BaseModel):
    """Health status for a single application component."""

    status: Literal["ok", "error"] = Field(description="Component status.")
    detail: str = Field(description="Human-readable component status detail.")


class HealthResponse(BaseModel):
    """Application health response."""

    status: Literal["ok", "degraded"] = Field(description="Overall application status.")
    application: ComponentHealth
    database: ComponentHealth
    redis: ComponentHealth