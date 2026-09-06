from dataclasses import dataclass, field

from simulator.swarm.vector import Vector2


@dataclass
class Obstacle:
    center: Vector2
    radius: float


@dataclass
class SwarmWorld:
    width: float
    height: float

    obstacles: list[Obstacle] = field(
        default_factory=list
    )

    target: Vector2 | None = None
