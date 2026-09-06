from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class SensorModel(Base):
    __tablename__ = "sensors"

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

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    sensor_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
