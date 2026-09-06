from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class AnomalyModel(Base):
    __tablename__ = "anomalies"

    id: Mapped[str] = mapped_column(
        String(64),
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

    sensor_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    anomaly_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )
