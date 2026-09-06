from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column


from app.infrastructure.database.base import Base


class RegionModel(Base):
    __tablename__ = "regions"

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
