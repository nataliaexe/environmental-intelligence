from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.event import EnvironmentalEvent
from app.domain.risk import RiskAssessment
from app.services.anomaly.fusion import AnomalyAssessment
from app.services.risk.engine import risk_engine


@dataclass(frozen=True)
class EventProcessingResult:
    event: EnvironmentalEvent
    risk: RiskAssessment


class EventEngine:

    def process_with_risk(
        self,
        region_id: str,
        assessment: AnomalyAssessment,
    ) -> EventProcessingResult | None:

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

        return EventProcessingResult(
            event=event,
            risk=risk,
        )

    def process(
        self,
        region_id: str,
        assessment: AnomalyAssessment,
    ) -> EnvironmentalEvent | None:

        result = self.process_with_risk(
            region_id=region_id,
            assessment=assessment,
        )

        if result is None:
            return None

        return result.event


event_engine = EventEngine()
