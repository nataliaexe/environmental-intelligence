from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class EnvironmentSnapshotModel(Base):
    __tablename__ = "environment_snapshots"

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

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    values: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    confidence: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    active_hazards: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    uncertainty: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    observability: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )
