from dataclasses import dataclass


@dataclass(frozen=True)
class AgentBelief:
    agent_id: str
    value: float
    confidence: float


@dataclass(frozen=True)
class ConsensusResult:
    value: float
    confidence: float
    agreement: float
    participants: int


def weighted_consensus(
    beliefs: list[AgentBelief],
) -> ConsensusResult:
    if not beliefs:
        return ConsensusResult(
            value=0.0,
            confidence=0.0,
            agreement=0.0,
            participants=0,
        )

    total_weight = sum(
        max(0.0, belief.confidence)
        for belief in beliefs
    )

    if total_weight == 0:
        return ConsensusResult(
            value=0.0,
            confidence=0.0,
            agreement=0.0,
            participants=len(beliefs),
        )

    weighted_value = sum(
        belief.value * belief.confidence
        for belief in beliefs
    )

    value = weighted_value / total_weight

    deviations = [
        abs(belief.value - value)
        for belief in beliefs
    ]

    average_deviation = (
        sum(deviations)
        / len(deviations)
    )

    agreement = max(
        0.0,
        1.0 - average_deviation,
    )

    confidence = (
        agreement
        * min(
            total_weight / len(beliefs),
            1.0,
        )
    )

    return ConsensusResult(
        value=round(value, 4),
        confidence=round(confidence, 4),
        agreement=round(agreement, 4),
        participants=len(beliefs),
    )
