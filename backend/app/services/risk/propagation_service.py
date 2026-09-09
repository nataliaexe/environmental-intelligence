from datetime import datetime, timezone

from app.infrastructure.database.repositories.risk import (
    risk_repository,
)
from app.services.risk_graph.catalog import RISK_GRAPH
from app.services.risk_graph.normalization import (
    normalize_hazard,
)
from app.services.risk_graph.propagation import (
    risk_graph_engine,
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
        initial_risk=None,
    ):

        normalized_hazard = normalize_hazard(
            initial_hazard,
        )

        assessments = []

        # Persist the initial risk if one was
        # already calculated by RiskEngine.
        if (
            session is not None
            and initial_risk is not None
        ):
            assessments.append(
                risk_repository.add(
                    session=session,
                    region_id=(
                        initial_risk.region_id
                    ),
                    event_id=event_id,
                    hazard_type=(
                        normalized_hazard
                    ),
                    risk_score=(
                        initial_risk.risk_score
                    ),
                    probability=(
                        initial_risk.probability
                    ),
                    impact=(
                        initial_risk.impact
                    ),
                    confidence=(
                        initial_risk.confidence
                    ),
                    severity=(
                        initial_risk.severity
                    ),
                    created_at=datetime.now(
                        timezone.utc
                    ),
                )
            )

        propagation = (
            risk_graph_engine.propagate(
                graph=RISK_GRAPH,
                initial_risks={
                    normalized_hazard: (
                        initial_score
                    ),
                },
            )
        )

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

            if session is not None:
                assessment = (
                    risk_repository.add(
                        session=session,
                        region_id=region_id,
                        event_id=event_id,
                        hazard_type=result.hazard,
                        risk_score=(
                            result.propagated_score
                        ),
                        probability=(
                            result.propagated_score
                        ),
                        impact=(
                            result.propagated_score
                        ),
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

        if session is not None:
            session.commit()

        return assessments


risk_propagation_service = (
    RiskPropagationService()
)
