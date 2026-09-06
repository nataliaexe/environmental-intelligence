from dataclasses import dataclass

from app.api.schemas.telemetry import TelemetryPayload


@dataclass(frozen=True)
class EnvironmentalFeatures:
    temperature: float
    humidity: float
    soil_moisture: float
    light: float

    temperature_delta: float
    humidity_delta: float
    soil_moisture_delta: float
    light_delta: float


def extract_features(
    current: TelemetryPayload,
    previous: TelemetryPayload | None,
) -> EnvironmentalFeatures:
    if previous is None:
        return EnvironmentalFeatures(
            temperature=current.temperature,
            humidity=current.humidity,
            soil_moisture=current.soil_moisture,
            light=current.light,
            temperature_delta=0.0,
            humidity_delta=0.0,
            soil_moisture_delta=0.0,
            light_delta=0.0,
        )

    return EnvironmentalFeatures(
        temperature=current.temperature,
        humidity=current.humidity,
        soil_moisture=current.soil_moisture,
        light=current.light,
        temperature_delta=current.temperature - previous.temperature,
        humidity_delta=current.humidity - previous.humidity,
        soil_moisture_delta=current.soil_moisture - previous.soil_moisture,
        light_delta=current.light - previous.light,
    )
