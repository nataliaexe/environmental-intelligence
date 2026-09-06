from datetime import datetime

from pydantic import BaseModel, Field


class TelemetryPayload(BaseModel):
    sensor_id: str = Field(min_length=1)
    region_id: str = Field(min_length=1)

    timestamp: datetime

    temperature: float
    humidity: float = Field(ge=0, le=100)
    soil_moisture: float = Field(ge=0, le=100)
    light: float = Field(ge=0)
