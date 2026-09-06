from datetime import datetime, timezone
from uuid import uuid4

from app.domain.anomaly import Anomaly
from app.infrastructure.database.models.environment_snapshot import (
    EnvironmentSnapshotModel,
)
from app.infrastructure.database.repositories.environment_snapshot import (
    environment_snapshot_repository,
)


class WorldModelAnomalyService:

    def evaluate(
        self,
        snapshot: EnvironmentSnapshotModel,
    ) -> list[Anomaly]:
        anomalies: list[Anomaly] = []

        values = snapshot.values
        confidence = snapshot.confidence
        uncertainty = snapshot.uncertainty

        temperature = values.get("temperature")
        temperature_confidence = confidence.get(
            "temperature",
            0.0,
        )

        if (
            temperature is not None
            and temperature >= 35.0
            and temperature_confidence >= 0.7
        ):
            anomalies.append(
                Anomaly(
                    id=f"ANOM-{uuid4().hex[:12]}",
                    region_id=snapshot.region_id,
                    sensor_id="world_model",
                    timestamp=snapshot.timestamp
                    or datetime.now(timezone.utc),
                    anomaly_type="high_temperature",
                    severity="warning",
                    score=min(
                        1.0,
                        (temperature - 30.0) / 10.0,
                    ),
                    description=(
                        "World Model reports "
                        "high environmental temperature."
                    ),
                )
            )

        soil_moisture = values.get(
            "soil_moisture"
        )

        soil_confidence = confidence.get(
            "soil_moisture",
            0.0,
        )

        if (
            soil_moisture is not None
            and soil_moisture <= 25.0
            and soil_confidence >= 0.7
        ):
            anomalies.append(
                Anomaly(
                    id=f"ANOM-{uuid4().hex[:12]}",
                    region_id=snapshot.region_id,
                    sensor_id="world_model",
                    timestamp=snapshot.timestamp
                    or datetime.now(timezone.utc),
                    anomaly_type="low_soil_moisture",
                    severity="warning",
                    score=min(
                        1.0,
                        (30.0 - soil_moisture) / 30.0,
                    ),
                    description=(
                        "World Model reports "
                        "low soil moisture."
                    ),
                )
            )

        if (
            temperature is not None
            and temperature_confidence < 0.7
        ):
            _ = uncertainty.get(
                "temperature",
                0.0,
            )

        return anomalies


world_model_anomaly_service = (
    WorldModelAnomalyService()
)
