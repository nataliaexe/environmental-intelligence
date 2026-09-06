from sqlalchemy.orm import Session

from app.services.events.anomaly_to_event import (
    anomaly_to_event,
)
from app.infrastructure.database.repositories.event import (
    event_repository,
)


class EventPersistenceService:

    def create_from_anomaly(
        self,
        session: Session,
        anomaly,
    ):

        event_data = anomaly_to_event.convert(
            anomaly
        )

        event = event_repository.add(
            session=session,
            **event_data,
        )

        return event


event_persistence = EventPersistenceService()
