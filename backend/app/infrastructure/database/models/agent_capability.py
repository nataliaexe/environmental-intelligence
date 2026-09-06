from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class AgentCapabilityModel(Base):
    __tablename__ = "agent_capabilities"

    agent_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("agents.id", ondelete="CASCADE"),
        primary_key=True,
    )

    capability: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )
