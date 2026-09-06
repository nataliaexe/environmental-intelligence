from dataclasses import dataclass


@dataclass(frozen=True)
class SwarmConfig:
    neighbor_radius: float = 8.0
    separation_radius: float = 2.0

    separation_weight: float = 1.8
    alignment_weight: float = 1.0
    cohesion_weight: float = 0.8
    target_weight: float = 1.2
    obstacle_weight: float = 2.0

    max_speed: float = 1.0
    max_acceleration: float = 0.1

    energy_per_step: float = 0.02
