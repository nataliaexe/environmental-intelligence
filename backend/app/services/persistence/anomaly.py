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
    ) -> None:

        anomaly_repository.add(
            session=session,
            anomaly_id=anomaly.id,
            region_id=anomaly.region_id,
            sensor_id=anomaly.sensor_id,
            timestamp=anomaly.timestamp,
            anomaly_type=anomaly.anomaly_type,
            severity=anomaly.severity,
            score=anomaly.score,
            description=anomaly.description,
        )


anomaly_persistence = (
    AnomalyPersistenceService()
)
