from dataclasses import dataclass


@dataclass
class RiskAssessment:
    region_id: str

    hazard_type: str

    risk_score: float
    probability: float
    impact: float
    confidence: float

    severity: str

    contributing_factors: list[str]
