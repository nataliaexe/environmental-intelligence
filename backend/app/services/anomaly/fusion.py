from dataclasses import dataclass

from app.api.schemas.telemetry import TelemetryPayload
from app.services.anomaly.features import extract_features
from app.services.anomaly.result import DetectorResult
from app.services.anomaly.rules import detect_environmental_rules
from app.services.anomaly.statistical import detect_statistical_anomaly


@dataclass(frozen=True)
class AnomalyAssessment:
    anomaly: bool
    score: float
    severity: str
    reasons: list[str]
    detectors: list[DetectorResult]


def assess_anomaly(
    current: TelemetryPayload,
    previous: TelemetryPayload | None,
    history: list[TelemetryPayload],
) -> AnomalyAssessment:
    features = extract_features(
        current=current,
        previous=previous,
    )

    rule_result = detect_environmental_rules(features)

    statistical_result = detect_statistical_anomaly(
        current=current,
        history=history,
    )

    results = [
        rule_result,
        statistical_result,
    ]

    score = (
        rule_result.score * 0.6
        + statistical_result.score * 0.4
    )

    anomaly = any(
        result.anomaly
        for result in results
    )

    if score >= 0.75:
        severity = "critical"
    elif score >= 0.40:
        severity = "warning"
    else:
        severity = "normal"

    reasons = list(
        dict.fromkeys(
            reason
            for result in results
            for reason in result.reasons
        )
    )

    return AnomalyAssessment(
        anomaly=anomaly,
        score=round(score, 4),
        severity=severity,
        reasons=reasons,
        detectors=results,
    )
