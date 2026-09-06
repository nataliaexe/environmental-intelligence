from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.infrastructure.database.repositories.environment_snapshot import (
    environment_snapshot_repository,
)


class EnvironmentWorldModel:

    def publish_snapshot(
        self,
        session: Session,
        *,
        region_id: str,
        values: dict,
        confidence: dict,
        active_hazards: list,
        uncertainty: dict,
        observability: dict,
    ):

        latest = environment_snapshot_repository.latest(
            session=session,
            region_id=region_id,
        )

        next_version = (
            latest.version + 1
            if latest is not None
            else 1
        )

        return environment_snapshot_repository.add(
            session=session,
            region_id=region_id,
            version=next_version,
            timestamp=datetime.now(timezone.utc),
            values=values,
            confidence=confidence,
            active_hazards=active_hazards,
            uncertainty=uncertainty,
            observability=observability,
        )

    def latest(
        self,
        session: Session,
        *,
        region_id: str,
    ):

        return environment_snapshot_repository.latest(
            session=session,
            region_id=region_id,
        )


environment_world_model = EnvironmentWorldModel()
