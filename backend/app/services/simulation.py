from app.domain.simulation_contract import (
    SimulationScenarioType,
)


class SimulationService:
    def __init__(self) -> None:
        self._scenario: SimulationScenarioType | None = (
            None
        )
        self._active: bool = False
        self._elapsed_steps: int = 0

    def start(
        self,
        scenario: SimulationScenarioType,
    ) -> dict:
        self._scenario = scenario
        self._active = True
        self._elapsed_steps = 0

        return {
            "scenario": (
                self._scenario.value
                if self._scenario
                else None
            ),
            "active": self._active,
            "elapsed_steps": self._elapsed_steps,
        }

    def stop(self) -> dict:
        self._active = False

        return {
            "scenario": (
                self._scenario.value
                if self._scenario
                else None
            ),
            "active": self._active,
            "elapsed_steps": self._elapsed_steps,
        }

    def status(self) -> dict:
        return {
            "scenario": (
                self._scenario.value
                if self._scenario
                else None
            ),
            "active": self._active,
            "elapsed_steps": self._elapsed_steps,
        }


simulation_service = SimulationService()
