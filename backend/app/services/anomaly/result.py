from dataclasses import dataclass


@dataclass(frozen=True)
class DetectorResult:
    detector: str
    anomaly: bool
    score: float
    severity: str
    reasons: list[str]
