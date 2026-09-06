from dataclasses import dataclass


@dataclass(frozen=True)
class WorldModelAnomalyInput:
    region_id: str

    values: dict[str, float]

    confidence: dict[str, float]

    uncertainty: dict[str, float]

    active_hazards: list[str]

    version: int
