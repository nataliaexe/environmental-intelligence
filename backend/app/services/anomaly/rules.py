from app.services.anomaly.features import EnvironmentalFeatures
from app.services.anomaly.result import DetectorResult


def detect_environmental_rules(
    features: EnvironmentalFeatures,
) -> DetectorResult:
    score = 0.0
    reasons: list[str] = []

    if features.temperature >= 35:
        score += 0.30
        reasons.append("high_temperature")

    if features.humidity <= 35:
        score += 0.20
        reasons.append("low_humidity")

    if features.soil_moisture <= 25:
        score += 0.25
        reasons.append("low_soil_moisture")

    if features.temperature_delta >= 1.0:
        score += 0.10
        reasons.append("rapid_temperature_increase")

    if features.humidity_delta <= -2.0:
        score += 0.05
        reasons.append("rapid_humidity_decrease")

    if features.soil_moisture_delta <= -2.0:
        score += 0.10
        reasons.append("rapid_soil_moisture_decrease")

    score = min(score, 1.0)

    if score >= 0.75:
        severity = "critical"
    elif score >= 0.40:
        severity = "warning"
    else:
        severity = "normal"

    return DetectorResult(
        detector="environmental_rules",
        anomaly=score >= 0.40,
        score=score,
        severity=severity,
        reasons=reasons,
    )
