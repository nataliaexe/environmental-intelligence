from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.infrastructure.database.models.event import EventModel


class EventRepository:

    def add(
        self,
        session: Session,
        *,
        event_id: str,
        region_id: str,
        event_type: str,
        severity: str,
        confidence: float,
        status: str,
        created_at: datetime,
        updated_at: datetime,
    ) -> EventModel:

        event = EventModel(
            id=event_id,
            region_id=region_id,
            event_type=event_type,
            severity=severity,
            confidence=confidence,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

        session.add(event)

        return event

    def active_events(
        self,
        session: Session,
    ) -> list[EventModel]:

        statement = (
            select(EventModel)
            .where(EventModel.status == "active")
            .order_by(desc(EventModel.created_at))
        )

        return list(session.scalars(statement).all())

    def events_by_region(
        self,
        session: Session,
        *,
        region_id: str,
    ) -> list[EventModel]:

        statement = (
            select(EventModel)
            .where(EventModel.region_id == region_id)
            .order_by(desc(EventModel.created_at))
        )

        return list(session.scalars(statement).all())

    def latest_by_region(
        self,
        session: Session,
        *,
        region_id: str,
    ) -> EventModel | None:

        statement = (
            select(EventModel)
            .where(EventModel.region_id == region_id)
            .order_by(desc(EventModel.created_at))
            .limit(1)
        )

        return session.scalars(statement).first()


event_repository = EventRepository()
