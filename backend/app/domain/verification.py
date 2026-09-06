from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class VerificationResult:
    mission_id: str

    success: bool

    confidence: float

    evidence: list[str] = field(
        default_factory=list
    )

    timestamp: datetime | None = None
