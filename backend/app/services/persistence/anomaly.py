from sqlalchemy.orm import Session

from app.domain.anomaly import Anomaly
from app.infrastructure.database.repositories.anomaly import (
    anomaly_repository,
)


class AnomalyPersistenceService:

    def store(
        self,
        session: Session,
        anomaly: Anomaly,
    ):
        return anomaly_repository.add(
            session=session,
            anomaly_id=anomaly.id,
            region_id=anomaly.region_id,
            source_type=anomaly.source_type,
            source_id=anomaly.source_id,
            timestamp=anomaly.timestamp,
            anomaly_type=anomaly.anomaly_type,
            severity=anomaly.severity,
            score=anomaly.score,
            description=anomaly.description,
        )


anomaly_persistence = AnomalyPersistenceService()
