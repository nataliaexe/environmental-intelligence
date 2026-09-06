from dataclasses import dataclass
from enum import Enum


class AuthorizationStatus(str, Enum):
    AUTHORIZED = "authorized"
    DENIED = "denied"
    REQUIRES_HUMAN = "requires_human"


@dataclass(frozen=True)
class AuthorizationDecision:
    status: AuthorizationStatus
    reason: str
    policy_id: str
