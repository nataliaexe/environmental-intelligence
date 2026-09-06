from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SimulationRequest:
    region_id: str

    environment_version: int

    scenario_id: str

    duration_seconds: float


@dataclass(frozen=True)
class SimulationObservation:
    region_id: str

    timestamp: datetime

    source: str

    values: dict[str, float]

    confidence: dict[str, float]

    agent_id: str | None = None
