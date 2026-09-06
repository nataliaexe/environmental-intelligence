from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EnvironmentalValue:
    value: float
    unit: str

    confidence: float = 1.0

    source: str = "unknown"

    timestamp: datetime | None = None


@dataclass
class EnvironmentState:
    region_id: str

    timestamp: datetime

    values: dict[str, EnvironmentalValue] = field(
        default_factory=dict
    )

    active_hazards: list[str] = field(
        default_factory=list
    )

    uncertainty: dict[str, float] = field(
        default_factory=dict
    )

    observability: dict[str, float] = field(
        default_factory=dict
    )
