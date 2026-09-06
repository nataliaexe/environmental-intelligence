from pydantic import BaseModel

from simulator.scenarios.types import ScenarioType


class ScenarioRequest(BaseModel):
    scenario: ScenarioType
