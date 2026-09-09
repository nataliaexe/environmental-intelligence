from pydantic import BaseModel

from app.domain.simulation_contract import (
    SimulationScenarioType,
)


class ScenarioRequest(BaseModel):
    scenario: SimulationScenarioType
