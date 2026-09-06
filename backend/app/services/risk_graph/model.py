from dataclasses import dataclass


@dataclass(frozen=True)
class RiskEdge:
    source: str
    target: str

    probability_multiplier: float

    delay_seconds: float = 0.0

    description: str = ""


@dataclass
class RiskGraph:
    nodes: set[str]

    edges: list[RiskEdge]
