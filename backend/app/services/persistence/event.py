from sqlalchemy.orm import Session

from app.services.events.anomaly_to_event import (
    anomaly_to_event,
)
from app.infrastructure.database.repositories.event import (
    event_repository,
)


class EventPersistenceService:

    def create_from_event(
        self,
        session: Session,
        event,
    ):
        return event_repository.add(
            session=session,
            event_id=event.id,
            region_id=event.region_id,
            event_type=event.event_type,
            severity=event.severity,
            confidence=event.confidence,
            status=event.status,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )

    def create_from_anomaly(
        self,
        session: Session,
        anomaly,
    ):
        event_data = anomaly_to_event.convert(
            anomaly
        )

        return event_repository.add(
            session=session,
            **event_data,
        )


event_persistence = EventPersistenceService()
