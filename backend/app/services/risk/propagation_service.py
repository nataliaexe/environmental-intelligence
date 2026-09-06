from datetime import datetime, timezone

from app.services.risk_graph.catalog import RISK_GRAPH
from app.services.risk_graph.propagation import (
    risk_graph_engine,
)
from app.infrastructure.database.repositories.risk import (
    risk_repository,
)


class RiskPropagationService:

    def propagate(
        self,
        session,
        *,
        region_id: str,
        initial_hazard: str,
        initial_score: float,
        event_id: str | None = None,
    ):

        propagation = (
            risk_graph_engine.propagate(
                graph=RISK_GRAPH,
                initial_risks={
                    initial_hazard: initial_score,
                },
            )
        )

        assessments = []

        for result in propagation:

            confidence = min(
                1.0,
                max(
                    0.0,
                    result.propagated_score,
                ),
            )

            severity = (
                "critical"
                if result.propagated_score >= 0.8
                else "high"
                if result.propagated_score >= 0.6
                else "moderate"
                if result.propagated_score >= 0.4
                else "low"
            )

            assessment = (
                risk_repository.add(
                    session=session,
                    region_id=region_id,
                    event_id=event_id,
                    hazard_type=result.hazard,
                    risk_score=result.propagated_score,
                    probability=result.propagated_score,
                    impact=result.propagated_score,
                    confidence=confidence,
                    severity=severity,
                    created_at=datetime.now(
                        timezone.utc
                    ),
                )
            )

            assessments.append(
                assessment
            )

        session.commit()

        return assessments


risk_propagation_service = (
    RiskPropagationService()
)
