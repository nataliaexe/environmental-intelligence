from dataclasses import dataclass


@dataclass(frozen=True)
class BehaviorProfile:
    separation_weight: float
    alignment_weight: float
    cohesion_weight: float
    target_weight: float
    obstacle_weight: float
