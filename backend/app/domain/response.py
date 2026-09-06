from dataclasses import dataclass, field


@dataclass(frozen=True)
class ResponsePolicy:
    hazard_id: str

    preferred_actions: list[str] = field(
        default_factory=list
    )

    minimum_confidence: float = 0.7

    requires_human_confirmation: bool = False

    max_agent_risk: float = 0.5
