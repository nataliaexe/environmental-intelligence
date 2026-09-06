from dataclasses import dataclass, field
from datetime import datetime

from app.domain.mission_state import MissionState


@dataclass
class Mission:
    id: str

    objective: str
    region_id: str

    priority: float

    required_capabilities: list[str] = field(
        default_factory=list
    )

    assigned_agents: list[str] = field(
        default_factory=list
    )

    status: MissionState = MissionState.PENDING

    created_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    expires_at: datetime | None = None

    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if isinstance(self.status, str):
            self.status = MissionState(self.status)
