from sqlalchemy.orm import Session

from app.infrastructure.database.repositories.anomaly import (
    anomaly_repository,
)
from app.services.anomaly.world_model_service import (
    world_model_anomaly_service,
)


class AnomalyPipeline:

    def process_snapshot(
        self,
        session: Session,
        snapshot,
    ):

        anomalies = (
            world_model_anomaly_service.evaluate(
                snapshot
            )
        )

        for anomaly in anomalies:
            anomaly_repository.add(
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

        session.commit()

        return anomalies


anomaly_pipeline = AnomalyPipeline()
