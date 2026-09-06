from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.services.fusion.engine import SensorFusionEngine
from app.services.environment.world_model import (
    environment_world_model,
)


class EnvironmentPublisher:

    def __init__(
        self,
        fusion: SensorFusionEngine,
    ) -> None:
        self.fusion = fusion

    def publish_measurement(
        self,
        session: Session,
        *,
        region_id: str,
        variable: str,
        value: float,
        source: str,
        variance: float,
    ):

        fused = self.fusion.update(
            variable=variable,
            value=value,
            source=source,
            variance=variance,
        )

        previous = (
            environment_world_model.latest(
                session=session,
                region_id=region_id,
            )
        )

        values = (
            dict(previous.values)
            if previous is not None
            else {}
        )

        confidence = (
            dict(previous.confidence)
            if previous is not None
            else {}
        )

        uncertainty = (
            dict(previous.uncertainty)
            if previous is not None
            else {}
        )

        observability = (
            dict(previous.observability)
            if previous is not None
            else {}
        )

        hazards = (
            list(previous.active_hazards)
            if previous is not None
            else []
        )

        values[variable] = fused.value
        confidence[variable] = fused.confidence
        uncertainty[variable] = fused.variance

        observability[source] = min(
            1.0,
            max(
                observability.get(source, 0.0),
                confidence[variable],
            ),
        )

        snapshot = (
            environment_world_model.publish_snapshot(
                session=session,
                region_id=region_id,
                values=values,
                confidence=confidence,
                active_hazards=hazards,
                uncertainty=uncertainty,
                observability=observability,
            )
        )

        return snapshot, fused


environment_publisher = EnvironmentPublisher(
    fusion=SensorFusionEngine()
)
