from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.infrastructure.database.models.telemetry import (
    TelemetryModel,
)


class TelemetryRepository:

    def add(
        self,
        session: Session,
        *,
        sensor_id: str,
        region_id: str,
        occurred_at: datetime,
        received_at: datetime,
        processed_at: datetime | None = None,
        temperature: float,
        humidity: float,
        soil_moisture: float,
        light: float,
    ) -> TelemetryModel:

        telemetry = TelemetryModel(
            timestamp=occurred_at,
            sensor_id=sensor_id,
            region_id=region_id,
            temperature=temperature,
            humidity=humidity,
            soil_moisture=soil_moisture,
            light=light,
            occurred_at=occurred_at,
            received_at=received_at,
            processed_at=processed_at,
        )

        session.add(telemetry)

        return telemetry

    def latest(
        self,
        session: Session,
        limit: int = 50,
    ) -> list[TelemetryModel]:

        statement = (
            select(TelemetryModel)
            .order_by(
                desc(TelemetryModel.occurred_at)
            )
            .limit(limit)
        )

        return list(session.scalars(statement))

    def latest_by_sensor(
        self,
        session: Session,
        sensor_id: str,
    ) -> TelemetryModel | None:

        statement = (
            select(TelemetryModel)
            .where(
                TelemetryModel.sensor_id == sensor_id
            )
            .order_by(
                desc(TelemetryModel.occurred_at)
            )
            .limit(1)
        )

        return session.scalars(statement).first()


telemetry_repository = TelemetryRepository()
