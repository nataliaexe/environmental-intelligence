from simulator.environment import EnvironmentSimulator
from simulator.scenarios.types import ScenarioType


class SimulationService:
    def __init__(self) -> None:
        self.simulator = EnvironmentSimulator(seed=42)

    def start(self, scenario: ScenarioType) -> dict:
        self.simulator.start_scenario(scenario)

        state = self.simulator.scenario_engine.state

        return {
            "scenario": state.scenario,
            "active": state.active,
            "elapsed_steps": state.elapsed_steps,
        }

    def stop(self) -> dict:
        self.simulator.stop_scenario()

        state = self.simulator.scenario_engine.state

        return {
            "scenario": state.scenario,
            "active": state.active,
            "elapsed_steps": state.elapsed_steps,
        }

    def status(self) -> dict:
        state = self.simulator.scenario_engine.state

        return {
            "scenario": state.scenario,
            "active": state.active,
            "elapsed_steps": state.elapsed_steps,
        }


simulation_service = SimulationService()
