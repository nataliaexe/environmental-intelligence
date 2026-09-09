from dataclasses import dataclass
from enum import Enum


class SimulationScenarioType(str, Enum):
    HEATWAVE = "heatwave"
    DROUGHT = "drought"
    WILDFIRE = "wildfire"
    FLOOD = "flood"
    EARTHQUAKE = "earthquake"


class SimulationBehaviorProfile(str, Enum):
    INVESTIGATE = "investigate"
    INCREASE_COVERAGE = "increase_coverage"
    MAP_REGION = "map_region"
    CREATE_RELAY = "create_relay"
    EMERGENCY = "emergency"
    RETURN_TO_SAFE = "return_to_safe"


@dataclass(frozen=True)
class SimulationRequest:
    scenario: SimulationScenarioType


@dataclass(frozen=True)
class SimulationObservation:
    region_id: str
    variable: str
    value: float
    confidence: float
    source: str
    timestamp: str
