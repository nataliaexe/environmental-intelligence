from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.infrastructure.database.models.environment_snapshot import (
    EnvironmentSnapshotModel,
)


class EnvironmentSnapshotRepository:

    def add(
        self,
        session: Session,
        *,
        region_id: str,
        version: int,
        timestamp: datetime,
        values: dict,
        confidence: dict,
        active_hazards: list,
        uncertainty: dict,
        observability: dict,
    ) -> EnvironmentSnapshotModel:

        snapshot = EnvironmentSnapshotModel(
            region_id=region_id,
            version=version,
            timestamp=timestamp,
            values=values,
            confidence=confidence,
            active_hazards=active_hazards,
            uncertainty=uncertainty,
            observability=observability,
        )

        session.add(snapshot)

        return snapshot

    def latest(
        self,
        session: Session,
        *,
        region_id: str,
    ) -> EnvironmentSnapshotModel | None:

        statement = (
            select(EnvironmentSnapshotModel)
            .where(
                EnvironmentSnapshotModel.region_id
                == region_id
            )
            .order_by(
                desc(EnvironmentSnapshotModel.version)
            )
            .limit(1)
        )

        return session.scalars(
            statement
        ).first()


environment_snapshot_repository = (
    EnvironmentSnapshotRepository()
)
