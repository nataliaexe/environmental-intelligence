from fastapi import APIRouter

from app.services.event_engine import event_engine


router = APIRouter(
    prefix="/events",
    tags=["events"],
)


@router.get("")
async def get_events() -> list[dict]:
    return [
        {
            "id": event.id,
            "region_id": event.region_id,
            "event_type": event.event_type,
            "severity": event.severity,
            "confidence": event.confidence,
            "status": event.status,
            "created_at": event.created_at,
            "updated_at": event.updated_at,
            "evidence": event.evidence,
        }
        for event in event_engine.active_events()
    ]


@router.get("/region/{region_id}")
async def get_region_events(
    region_id: str,
) -> list[dict]:
    return [
        {
            "id": event.id,
            "region_id": event.region_id,
            "event_type": event.event_type,
            "severity": event.severity,
            "confidence": event.confidence,
            "status": event.status,
            "created_at": event.created_at,
            "updated_at": event.updated_at,
            "evidence": event.evidence,
        }
        for event in event_engine.events_by_region(region_id)
    ]
