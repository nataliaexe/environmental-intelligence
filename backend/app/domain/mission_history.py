from dataclasses import dataclass
from datetime import datetime

from app.domain.mission_state import MissionState


@dataclass(frozen=True)
class MissionTransition:
    mission_id: str

    from_state: MissionState | None
    to_state: MissionState

    timestamp: datetime

    reason: str
