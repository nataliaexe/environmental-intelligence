from fastapi import APIRouter

from app.api.schemas.telemetry import TelemetryPayload
from app.services.telemetry import telemetry_store


router = APIRouter(
    prefix="/telemetry",
    tags=["telemetry"],
)


@router.post("")
async def receive_telemetry(payload: TelemetryPayload) -> dict:
    telemetry_store.add(payload)

    return {
        "status": "accepted",
        "sensor_id": payload.sensor_id,
        "region_id": payload.region_id,
        "timestamp": payload.timestamp,
    }


@router.get("/latest")
async def get_latest_telemetry(limit: int = 50) -> list[TelemetryPayload]:
    limit = max(1, min(limit, 100))
    return telemetry_store.latest(limit)


@router.get("/sensor/{sensor_id}")
async def get_sensor_telemetry(sensor_id: str) -> TelemetryPayload | None:
    return telemetry_store.latest_by_sensor(sensor_id)
