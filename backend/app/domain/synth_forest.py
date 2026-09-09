from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SynthForestReading:
    id: str
    region_id: str

    co2_ppm: float
    oxygen_ppm: float
    solar_energy: float
    temperature: float

    timestamp: datetime

    source_type: str
    source_id: str
