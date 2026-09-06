from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EnvironmentalEvent:
    id: str
    region_id: str

    event_type: str
    severity: str

    confidence: float

    status: str
    created_at: datetime
    updated_at: datetime

    evidence: list[str] = field(default_factory=list)
