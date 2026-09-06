from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.infrastructure.database.models.observation import (
    ObservationModel,
)


class ObservationRepository:

    def add(
        self,
        session: Session,
        *,
        observation_id: str,
        region_id: str,
        source: str,
        source_id: str | None,
        variable: str,
        value: float,
        confidence: float,
        occurred_at: datetime,
        received_at: datetime,
        processed_at: datetime | None = None,
        vector_clock: str | None = None,
    ) -> ObservationModel:

        observation = ObservationModel(
            id=observation_id,
            region_id=region_id,
            source=source,
            source_id=source_id,
            variable=variable,
            value=value,
            confidence=confidence,
            occurred_at=occurred_at,
            received_at=received_at,
            processed_at=processed_at,
            vector_clock=vector_clock,
        )

        session.add(observation)

        return observation

    def latest(
        self,
        session: Session,
        *,
        region_id: str | None = None,
        limit: int = 50,
    ) -> list[ObservationModel]:

        statement = select(
            ObservationModel
        ).order_by(
            desc(ObservationModel.occurred_at)
        )

        if region_id is not None:
            statement = statement.where(
                ObservationModel.region_id
                == region_id
            )

        statement = statement.limit(limit)

        return list(session.scalars(statement))

    def latest_by_variable(
        self,
        session: Session,
        *,
        region_id: str,
        variable: str,
    ) -> ObservationModel | None:

        statement = (
            select(ObservationModel)
            .where(
                ObservationModel.region_id
                == region_id,
                ObservationModel.variable
                == variable,
            )
            .order_by(
                desc(ObservationModel.occurred_at)
            )
            .limit(1)
        )

        return session.scalars(
            statement
        ).first()


observation_repository = ObservationRepository()
