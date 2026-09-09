from enum import Enum


class MissionState(str, Enum):
    PENDING = "pending"
    PLANNED = "planned"
    AWAITING_APPROVAL = "awaiting_approval"
    AUTHORIZED = "authorized"
    ASSIGNED = "assigned"
    EXECUTING = "executing"
    OBSERVING = "observing"
    VERIFYING = "verifying"
    COMPLETED = "completed"

    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
