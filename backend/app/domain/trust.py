from enum import Enum


class TrustState(str, Enum):
    TRUSTED = "trusted"
    DEGRADED = "degraded"
    SUSPICIOUS = "suspicious"
    QUARANTINED = "quarantined"
    REVOKED = "revoked"
