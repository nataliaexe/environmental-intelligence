from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EnvironmentSnapshot:
    region_id: str

    timestamp: datetime

    values: dict[str, float]

    confidence: dict[str, float]

    active_hazards: tuple[str, ...]

    version: int
