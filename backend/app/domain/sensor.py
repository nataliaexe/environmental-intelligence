from dataclasses import dataclass
from datetime import datetime


@dataclass
class Sensor:
    id: str
    region_id: str
    name: str
    sensor_type: str
    status: str
    last_seen: datetime | None = None
