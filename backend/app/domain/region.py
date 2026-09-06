from dataclasses import dataclass


@dataclass
class Region:
    id: str
    name: str

    latitude: float
    longitude: float

    health_score: float = 1.0
