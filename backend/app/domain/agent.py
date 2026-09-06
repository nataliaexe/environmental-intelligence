from dataclasses import dataclass, field
from enum import Enum


class AgentState(str, Enum):
    OFFLINE = "offline"
    IDLE = "idle"
    MOVING = "moving"
    OBSERVING = "observing"
    EXECUTING = "executing"
    RETURNING = "returning"
    CHARGING = "charging"
    QUARANTINED = "quarantined"
    FAILED = "failed"


@dataclass
class AgentEnergy:
    level: float = 100.0
    health: float = 100.0


@dataclass
class AgentLocalization:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    accuracy: float = 1.0
    confidence: float = 1.0


@dataclass
class EnvironmentalAgent:
    id: str
    name: str

    state: AgentState = AgentState.IDLE

    capabilities: list[str] = field(
        default_factory=list
    )

    localization: AgentLocalization = field(
        default_factory=AgentLocalization
    )

    energy: AgentEnergy = field(
        default_factory=AgentEnergy
    )

    trust_score: float = 1.0

    current_mission_id: str | None = None
