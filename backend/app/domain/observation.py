from dataclasses import dataclass
from datetime import datetime


@dataclass
class EnvironmentalObservation:
    sensor_id: str
    region_id: str
    timestamp: datetime

    temperature: float
    humidity: float
    soil_moisture: float
    light: float
