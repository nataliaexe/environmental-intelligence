from dataclasses import dataclass

from simulator.scenarios.config import SCENARIOS, ScenarioConfig
from simulator.scenarios.types import ScenarioType


@dataclass
class ScenarioState:
    scenario: ScenarioType
    elapsed_steps: int = 0
    active: bool = False


class ScenarioEngine:
    def __init__(self) -> None:
        self.state = ScenarioState(
            scenario=ScenarioType.NORMAL,
            active=False,
        )

    @property
    def config(self) -> ScenarioConfig:
        return SCENARIOS[self.state.scenario]

    def start(self, scenario: ScenarioType) -> None:
        self.state = ScenarioState(
            scenario=scenario,
            elapsed_steps=0,
            active=scenario != ScenarioType.NORMAL,
        )

    def stop(self) -> None:
        self.state = ScenarioState(
            scenario=ScenarioType.NORMAL,
            elapsed_steps=0,
            active=False,
        )

    def step(self) -> ScenarioState:
        if not self.state.active:
            return self.state

        self.state.elapsed_steps += 1

        if (
            self.config.duration_steps > 0
            and self.state.elapsed_steps >= self.config.duration_steps
        ):
            self.stop()

        return self.state
