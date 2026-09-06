from datetime import datetime, timezone

from app.domain.mission import Mission
from app.domain.verification import VerificationResult


class MissionVerificationService:

    def verify(
        self,
        mission: Mission,
        success: bool,
        confidence: float,
        evidence: list[str],
    ) -> VerificationResult:

        confidence = max(
            0.0,
            min(confidence, 1.0),
        )

        return VerificationResult(
            mission_id=mission.id,
            success=success,
            confidence=confidence,
            evidence=evidence,
            timestamp=datetime.now(
                timezone.utc
            ),
        )


mission_verification = (
    MissionVerificationService()
)
