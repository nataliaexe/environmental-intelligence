from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TerraFormerReading:
    id: str
    region_id: str

    soil_moisture: float
    soil_ph: float
    organic_matter: float
    compaction: float
    biodiversity_index: float

    timestamp: datetime

    source_type: str
    source_id: str
