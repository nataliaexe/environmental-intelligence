from fastapi import FastAPI

from app.api.routes.environment import router as environment_router
from app.api.routes.events import router as events_router
from app.api.routes.simulation import router as simulation_router
from app.api.routes.telemetry import router as telemetry_router
from app.core.config import get_settings


settings = get_settings()


app = FastAPI(
    title=settings.project_name,
    description="Environmental Intelligence & Resilience Platform",
    version=settings.project_version,
)


app.include_router(environment_router, prefix="/api")
app.include_router(telemetry_router, prefix="/api")
app.include_router(simulation_router, prefix="/api")
app.include_router(events_router, prefix="/api")


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.project_name,
        "status": "online",
        "version": settings.project_version,
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "environment": settings.environment,
    }
