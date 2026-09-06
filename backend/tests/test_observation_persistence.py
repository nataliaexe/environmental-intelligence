from datetime import datetime, timezone
from uuid import uuid4

from app.infrastructure.database.session import (
    engine,
)
from app.infrastructure.database.repositories.observation import (
    observation_repository,
)
from app.infrastructure.database.dependencies import (
    SessionLocal,
)


def test_observation_can_be_persisted(
    test_sensor: dict[str, str],
) -> None:

    observation_id = str(uuid4())
    occurred_at = datetime.now(timezone.utc)

    session = SessionLocal()

    try:
        observation_repository.add(
            session=session,
            observation_id=observation_id,
            region_id=test_sensor["region_id"],
            source="fixed_sensor",
            source_id=test_sensor["sensor_id"],
            variable="temperature",
            value=31.4,
            confidence=0.98,
            occurred_at=occurred_at,
            received_at=occurred_at,
            vector_clock='{"TEST-SENSOR": 1}',
        )

        session.commit()

        result = (
            observation_repository.latest_by_variable(
                session=session,
                region_id=test_sensor["region_id"],
                variable="temperature",
            )
        )

        assert result is not None
        assert result.id == observation_id
        assert result.value == 31.4
        assert result.confidence == 0.98

    finally:
        session.close()

        with engine.begin() as connection:
            from sqlalchemy import text

            connection.execute(
                text(
                    """
                    DELETE FROM observations
                    WHERE id = :id
                    """
                ),
                {
                    "id": observation_id,
                },
            )
