from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class AgentPositionHistoryModel(Base):
    __tablename__ = "agent_position_history"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )

    agent_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("agents.id", ondelete="CASCADE"),
        primary_key=True,
    )

    x: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    y: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    z: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    accuracy: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
