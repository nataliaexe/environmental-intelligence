from app.api.schemas.telemetry import TelemetryPayload
from app.services.anomaly.fusion import (
    AnomalyAssessment,
    assess_anomaly,
)


class AnomalyService:
    def assess(
        self,
        payload: TelemetryPayload,
        history: list[TelemetryPayload] | None = None,
    ) -> AnomalyAssessment:
        previous = history[-1] if history else None

        return assess_anomaly(
            current=payload,
            previous=previous,
            history=history or [],
        )


anomaly_service = AnomalyService()
