from math import sqrt

from app.api.schemas.telemetry import TelemetryPayload
from app.services.anomaly.result import DetectorResult


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _std(values: list[float], mean: float) -> float:
    if len(values) < 2:
        return 0.0

    variance = sum(
        (value - mean) ** 2
        for value in values
    ) / len(values)

    return sqrt(variance)


def _z_score(
    value: float,
    history: list[float],
) -> float:
    if len(history) < 3:
        return 0.0

    mean = _mean(history)
    std = _std(history, mean)

    if std == 0:
        return 0.0

    return abs(value - mean) / std


def detect_statistical_anomaly(
    current: TelemetryPayload,
    history: list[TelemetryPayload],
) -> DetectorResult:
    temperatures = [
        item.temperature
        for item in history
    ]

    humidity = [
        item.humidity
        for item in history
    ]

    soil = [
        item.soil_moisture
        for item in history
    ]

    temperature_z = _z_score(
        current.temperature,
        temperatures,
    )

    humidity_z = _z_score(
        current.humidity,
        humidity,
    )

    soil_z = _z_score(
        current.soil_moisture,
        soil,
    )

    maximum_z = max(
        temperature_z,
        humidity_z,
        soil_z,
    )

    score = min(maximum_z / 3.0, 1.0)

    reasons: list[str] = []

    if temperature_z >= 3:
        reasons.append(
            "temperature_statistical_outlier"
        )

    if humidity_z >= 3:
        reasons.append(
            "humidity_statistical_outlier"
        )

    if soil_z >= 3:
        reasons.append(
            "soil_moisture_statistical_outlier"
        )

    anomaly = maximum_z >= 3

    if not anomaly:
        severity = "normal"
    elif score >= 0.75:
        severity = "critical"
    elif score >= 0.50:
        severity = "warning"
    else:
        severity = "normal"

    return DetectorResult(
        detector="statistical",
        anomaly=anomaly,
        score=round(score, 4),
        severity=severity,
        reasons=reasons,
    )
