from dataclasses import dataclass, field

from simulator.swarm.vector import Vector2


@dataclass
class SimulatedAgent:
    agent_id: str

    position: Vector2 = field(
        default_factory=Vector2
    )

    velocity: Vector2 = field(
        default_factory=Vector2
    )

    acceleration: Vector2 = field(
        default_factory=Vector2
    )

    navigation_target: Vector2 | None = None

    max_speed: float = 1.0
    max_acceleration: float = 0.1

    energy: float = 100.0

    active: bool = True
