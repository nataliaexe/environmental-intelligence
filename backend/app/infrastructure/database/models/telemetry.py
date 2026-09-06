from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class TelemetryModel(Base):
    __tablename__ = "telemetry"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )

    sensor_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(
            "sensors.id",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )

    region_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(
            "regions.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    humidity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    soil_moisture: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    light: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
