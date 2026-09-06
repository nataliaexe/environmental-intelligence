from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column


from app.infrastructure.database.base import Base


class AgentModel(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    energy_level: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=100.0,
    )

    energy_health: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=100.0,
    )

    trust_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
    )

    x: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    y: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    z: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    current_mission_id: Mapped[str | None] = (
        mapped_column(
            String(64),
            nullable=True,
        )
    )
