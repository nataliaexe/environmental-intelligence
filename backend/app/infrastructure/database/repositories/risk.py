from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.infrastructure.database.models.risk_assessment import (
    RiskAssessmentModel,
)


class RiskRepository:

    def add(
        self,
        session: Session,
        *,
        region_id: str,
        event_id: str | None,
        hazard_type: str,
        risk_score: float,
        probability: float,
        impact: float,
        confidence: float,
        severity: str,
        created_at: datetime,
    ) -> RiskAssessmentModel:

        risk = RiskAssessmentModel(
            region_id=region_id,
            event_id=event_id,
            hazard_type=hazard_type,
            risk_score=risk_score,
            probability=probability,
            impact=impact,
            confidence=confidence,
            severity=severity,
            created_at=created_at,
        )

        session.add(risk)

        return risk

    def latest_by_region(
        self,
        session: Session,
        *,
        region_id: str,
    ) -> RiskAssessmentModel | None:

        statement = (
            select(RiskAssessmentModel)
            .where(
                RiskAssessmentModel.region_id
                == region_id
            )
            .order_by(
                desc(
                    RiskAssessmentModel.created_at
                )
            )
            .limit(1)
        )

        return session.scalars(statement).first()


risk_repository = RiskRepository()
