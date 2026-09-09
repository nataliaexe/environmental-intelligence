from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.telemetry import TelemetryPayload
from app.infrastructure.database.dependencies import (
    get_db,
)
from app.infrastructure.database.repositories.telemetry import (
    telemetry_repository,
)
from app.services.persistence.telemetry import (
    telemetry_persistence,
)


router = APIRouter(
    prefix="/telemetry",
    tags=["telemetry"],
)


def _telemetry_to_dict(record) -> dict:
    return {
        "sensor_id": record.sensor_id,
        "region_id": record.region_id,
        "occurred_at": record.occurred_at,
        "received_at": record.received_at,
        "processed_at": record.processed_at,
        "temperature": record.temperature,
        "humidity": record.humidity,
        "soil_moisture": record.soil_moisture,
        "light": record.light,
    }


@router.post("")
async def receive_telemetry(
    payload: TelemetryPayload,
    session: Session = Depends(get_db),
) -> dict:

    telemetry_persistence.store(
        session=session,
        payload=payload,
    )

    session.commit()

    return {
        "status": "accepted",
        "sensor_id": payload.sensor_id,
        "region_id": payload.region_id,
        "occurred_at": payload.timestamp,
    }


@router.get("/latest")
async def get_latest_telemetry(
    limit: int = 50,
    session: Session = Depends(get_db),
) -> list[dict]:

    limit = max(
        1,
        min(limit, 100),
    )

    records = telemetry_repository.latest(
        session=session,
        limit=limit,
    )

    return [
        _telemetry_to_dict(record)
        for record in records
    ]


@router.get("/sensor/{sensor_id}")
async def get_sensor_telemetry(
    sensor_id: str,
    session: Session = Depends(get_db),
) -> dict | None:

    record = telemetry_repository.latest_by_sensor(
        session=session,
        sensor_id=sensor_id,
    )

    if record is None:
        return None

    return _telemetry_to_dict(record)
