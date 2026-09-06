from dataclasses import dataclass, field

from app.domain.authorization import AuthorizationDecision
from app.domain.mission import Mission
from app.domain.task import AgentTask
from app.domain.verification import VerificationResult


@dataclass
class OrchestrationResult:
    mission: Mission

    authorization: list[AuthorizationDecision] = field(
        default_factory=list
    )

    tasks: list[AgentTask] = field(
        default_factory=list
    )

    verification: VerificationResult | None = None

    success: bool = False

    reason: str | None = None
