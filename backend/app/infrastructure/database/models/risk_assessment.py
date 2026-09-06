from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class RiskAssessmentModel(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    region_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("regions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    event_id: Mapped[str | None] = (
        mapped_column(
            String(64),
            ForeignKey(
                "environmental_events.id",
                ondelete="SET NULL",
            ),
            nullable=True,
            index=True,
        )
    )

    hazard_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    impact: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
