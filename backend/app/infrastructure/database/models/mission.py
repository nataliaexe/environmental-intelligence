from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class MissionModel(Base):
    __tablename__ = "missions"

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
    )

    objective: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
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

    priority: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime | None] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=True,
        )
    )

    started_at: Mapped[datetime | None] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=True,
        )
    )

    completed_at: Mapped[datetime | None] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=True,
        )
    )

    expires_at: Mapped[datetime | None] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=True,
        )
    )

    failure_reason: Mapped[str | None] = (
        mapped_column(
            String(500),
            nullable=True,
        )
    )
