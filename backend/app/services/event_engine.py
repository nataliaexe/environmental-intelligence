from datetime import datetime, timezone
from uuid import uuid4

from app.domain.event import EnvironmentalEvent
from app.services.anomaly.fusion import AnomalyAssessment
from app.services.events import event_store
from app.services.risk.engine import risk_engine


class EventEngine:
    def process(
        self,
        region_id: str,
        assessment: AnomalyAssessment,
    ) -> EnvironmentalEvent | None:
        if not assessment.anomaly:
            return None

        now = datetime.now(timezone.utc)

        risk = risk_engine.assess(
            region_id=region_id,
            anomaly=assessment,
        )

        event = EnvironmentalEvent(
            id=f"EVENT-{uuid4().hex[:8].upper()}",
            region_id=region_id,
            event_type=risk.hazard_type,
            severity=risk.severity,
            confidence=risk.confidence,
            status="active",
            created_at=now,
            updated_at=now,
            evidence=risk.contributing_factors,
        )

        event_store.add(event)

        return event

    def active_events(self) -> list[EnvironmentalEvent]:
        return event_store.active()

    def events_by_region(
        self,
        region_id: str,
    ) -> list[EnvironmentalEvent]:
        return event_store.by_region(region_id)


event_engine = EventEngine()
