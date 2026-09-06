from app.api.schemas.telemetry import TelemetryPayload
from app.services.anomaly.fusion import AnomalyAssessment, assess_anomaly
from app.services.telemetry import telemetry_store


class AnomalyService:
    def assess(self, payload: TelemetryPayload) -> AnomalyAssessment:
        history = telemetry_store.history_by_sensor(
            payload.sensor_id
        )

        previous = history[-1] if history else None

        return assess_anomaly(
            current=payload,
            previous=previous,
            history=history,
        )


anomaly_service = AnomalyService()
