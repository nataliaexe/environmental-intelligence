from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EventTime:
    occurred_at: datetime
    received_at: datetime
    processed_at: datetime
