from dataclasses import dataclass

from simulator.scenarios.types import ScenarioType


@dataclass(frozen=True)
class ScenarioConfig:
    scenario: ScenarioType
    temperature_delta: float = 0.0
    humidity_delta: float = 0.0
    soil_moisture_delta: float = 0.0
    light_delta: float = 0.0
    duration_steps: int = 0


SCENARIOS: dict[ScenarioType, ScenarioConfig] = {
    ScenarioType.NORMAL: ScenarioConfig(
        scenario=ScenarioType.NORMAL,
    ),
    ScenarioType.HEATWAVE: ScenarioConfig(
        scenario=ScenarioType.HEATWAVE,
        temperature_delta=0.7,
        humidity_delta=-1.0,
        soil_moisture_delta=-0.6,
        light_delta=18.0,
        duration_steps=30,
    ),
    ScenarioType.DROUGHT: ScenarioConfig(
        scenario=ScenarioType.DROUGHT,
        temperature_delta=0.3,
        humidity_delta=-1.2,
        soil_moisture_delta=-1.2,
        light_delta=10.0,
        duration_steps=40,
    ),
    ScenarioType.HEAVY_RAIN: ScenarioConfig(
        scenario=ScenarioType.HEAVY_RAIN,
        temperature_delta=-0.4,
        humidity_delta=2.0,
        soil_moisture_delta=2.5,
        light_delta=-35.0,
        duration_steps=20,
    ),
    ScenarioType.SENSOR_FAILURE: ScenarioConfig(
        scenario=ScenarioType.SENSOR_FAILURE,
        duration_steps=15,
    ),
    ScenarioType.SENSOR_DRIFT: ScenarioConfig(
        scenario=ScenarioType.SENSOR_DRIFT,
        duration_steps=30,
    ),
}
