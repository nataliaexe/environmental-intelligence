from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AquaLeafReading:
    id: str
    region_id: str

    co2_dissolved: float
    oxygen_dissolved: float
    ph: float
    temperature: float

    timestamp: datetime

    source_type: str
    source_id: str
