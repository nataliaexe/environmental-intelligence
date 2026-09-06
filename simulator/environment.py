from dataclasses import dataclass
import random

from simulator.scenarios.engine import ScenarioEngine
from simulator.scenarios.types import ScenarioType


@dataclass
class EnvironmentalState:
    temperature: float
    humidity: float
    soil_moisture: float
    light: float


class EnvironmentSimulator:
    def __init__(
        self,
        initial_state: EnvironmentalState | None = None,
        seed: int | None = None,
    ) -> None:
        self.random = random.Random(seed)

        self.state = initial_state or EnvironmentalState(
            temperature=27.0,
            humidity=65.0,
            soil_moisture=55.0,
            light=700.0,
        )

        self.scenario_engine = ScenarioEngine()

    def start_scenario(self, scenario: ScenarioType) -> None:
        self.scenario_engine.start(scenario)

    def stop_scenario(self) -> None:
        self.scenario_engine.stop()

    def step(self) -> EnvironmentalState:
        scenario_state = self.scenario_engine.step()
        config = self.scenario_engine.config

        self.state.temperature += self.random.uniform(-0.4, 0.4)
        self.state.humidity += self.random.uniform(-1.0, 1.0)
        self.state.soil_moisture += self.random.uniform(-0.8, 0.8)
        self.state.light += self.random.uniform(-30.0, 30.0)

        if scenario_state.active:
            self.state.temperature += config.temperature_delta
            self.state.humidity += config.humidity_delta
            self.state.soil_moisture += config.soil_moisture_delta
            self.state.light += config.light_delta

        if scenario_state.scenario == ScenarioType.SENSOR_FAILURE:
            self.state.temperature = 999.0
            self.state.humidity = 999.0
            self.state.soil_moisture = 999.0
            self.state.light = 999.0

        elif scenario_state.scenario == ScenarioType.SENSOR_DRIFT:
            self.state.temperature += 0.2
            self.state.humidity -= 0.2
            self.state.soil_moisture -= 0.15

        self.state.humidity = max(0.0, min(100.0, self.state.humidity))
        self.state.soil_moisture = max(0.0, min(100.0, self.state.soil_moisture))
        self.state.light = max(0.0, self.state.light)

        return self.state
