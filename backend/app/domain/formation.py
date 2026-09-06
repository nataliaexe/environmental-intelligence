from enum import Enum


class FormationType(str, Enum):
    DISTRIBUTED = "distributed"
    CONVERGED = "converged"
    LINE = "line"
    GRID = "grid"
    RING = "ring"
    RELAY = "relay"
