from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.api.schemas.telemetry import TelemetryPayload
from app.infrastructure.database.repositories.telemetry import (
    telemetry_repository,
)


class TelemetryPersistenceService:

    def store(
        self,
        session: Session,
        payload: TelemetryPayload,
    ) -> None:

        now = datetime.now(timezone.utc)

        telemetry_repository.add(
            session=session,
            sensor_id=payload.sensor_id,
            region_id=payload.region_id,
            occurred_at=payload.timestamp,
            received_at=now,
            processed_at=now,
            temperature=payload.temperature,
            humidity=payload.humidity,
            soil_moisture=payload.soil_moisture,
            light=payload.light,
        )


telemetry_persistence = (
    TelemetryPersistenceService()
)
