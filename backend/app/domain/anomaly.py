from dataclasses import dataclass
from datetime import datetime


@dataclass
class Anomaly:
    id: str
    region_id: str

    source_type: str
    source_id: str

    timestamp: datetime

    anomaly_type: str
    severity: str

    score: float
    description: str
