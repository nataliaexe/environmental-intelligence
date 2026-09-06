from datetime import datetime, timezone
from uuid import uuid4

from app.domain.anomaly import Anomaly


class AnomalyToEvent:

    EVENT_MAP = {
        "high_temperature": "heatwave_risk",
        "low_soil_moisture": "drought_risk",
        "low_humidity": "dry_conditions",
        "rapid_temperature_increase": "thermal_event",
        "rapid_humidity_decrease": "drying_event",
        "rapid_soil_moisture_decrease": (
            "soil_drying_event"
        ),
    }

    def convert(
        self,
        anomaly: Anomaly,
    ) -> dict:

        event_type = self.EVENT_MAP.get(
            anomaly.anomaly_type,
            "environmental_anomaly",
        )

        return {
            "id": f"EVENT-{uuid4().hex[:12]}",
            "region_id": anomaly.region_id,
            "event_type": event_type,
            "severity": anomaly.severity,
            "confidence": min(
                1.0,
                max(0.0, anomaly.score),
            ),
            "status": "active",
            "created_at": anomaly.timestamp,
            "updated_at": datetime.now(timezone.utc),
        }


anomaly_to_event = AnomalyToEvent()
