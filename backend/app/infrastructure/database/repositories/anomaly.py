from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.infrastructure.database.models.anomaly import (
    AnomalyModel,
)


class AnomalyRepository:

    def add(
        self,
        session: Session,
        *,
        anomaly_id: str,
        region_id: str,
        source_type: str,
        source_id: str,
        timestamp: datetime,
        anomaly_type: str,
        severity: str,
        score: float,
        description: str,
    ) -> AnomalyModel:

        anomaly = AnomalyModel(
            id=anomaly_id,
            region_id=region_id,
            source_type=source_type,
            source_id=source_id,
            timestamp=timestamp,
            anomaly_type=anomaly_type,
            severity=severity,
            score=score,
            description=description,
        )

        session.add(anomaly)

        return anomaly

    def latest(
        self,
        session: Session,
        *,
        region_id: str | None = None,
        limit: int = 50,
    ) -> list[AnomalyModel]:

        statement = select(
            AnomalyModel
        ).order_by(
            desc(AnomalyModel.timestamp)
        )

        if region_id is not None:
            statement = statement.where(
                AnomalyModel.region_id == region_id
            )

        statement = statement.limit(limit)

        return list(session.scalars(statement))

    def latest_by_region(
        self,
        session: Session,
        *,
        region_id: str,
    ) -> AnomalyModel | None:

        statement = (
            select(AnomalyModel)
            .where(
                AnomalyModel.region_id == region_id
            )
            .order_by(
                desc(AnomalyModel.timestamp)
            )
            .limit(1)
        )

        return session.scalars(statement).first()


anomaly_repository = AnomalyRepository()
