from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.database.dependencies import get_db
from app.infrastructure.database.models.event import EventModel
from app.infrastructure.database.models.event_evidence import (
    EventEvidenceModel,
)
from app.infrastructure.database.repositories.event import (
    event_repository,
)


router = APIRouter(
    prefix="/events",
    tags=["events"],
)


def _event_to_dict(
    event: EventModel,
    db: Session,
) -> dict:

    evidence_statement = (
        select(EventEvidenceModel)
        .where(EventEvidenceModel.event_id == event.id)
    )

    evidence = [
        {
            "source": item.source,
            "reason": item.reason,
        }
        for item in db.scalars(evidence_statement).all()
    ]

    return {
        "id": event.id,
        "region_id": event.region_id,
        "event_type": event.event_type,
        "severity": event.severity,
        "confidence": event.confidence,
        "status": event.status,
        "created_at": event.created_at,
        "updated_at": event.updated_at,
        "evidence": evidence,
    }


@router.get("")
async def get_events(
    db: Session = Depends(get_db),
) -> list[dict]:
    events = event_repository.active_events(db)
    return [_event_to_dict(event, db) for event in events]


@router.get("/region/{region_id}")
async def get_region_events(
    region_id: str,
    db: Session = Depends(get_db),
) -> list[dict]:
    events = event_repository.events_by_region(
        db,
        region_id=region_id,
    )
    return [_event_to_dict(event, db) for event in events]
