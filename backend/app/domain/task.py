from dataclasses import dataclass
from datetime import datetime

from app.domain.mission_state import MissionState


@dataclass
class AgentTask:
    id: str

    mission_id: str
    agent_id: str

    objective: str

    status: MissionState = MissionState.ASSIGNED

    created_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    failure_reason: str | None = None
