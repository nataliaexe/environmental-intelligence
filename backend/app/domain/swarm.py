from dataclasses import dataclass, field


@dataclass
class SwarmObjective:
    type: str

    target_region_id: str | None = None

    priority: float = 0.0

    target_coverage: float = 1.0

    target_x: float | None = None
    target_y: float | None = None

    minimum_agents: int = 1

    required_capabilities: list[str] = field(
        default_factory=list
    )


@dataclass
class Swarm:
    id: str

    agents: list[str] = field(
        default_factory=list
    )

    objective: SwarmObjective | None = None

    formation: str = "distributed"

    coverage: float = 0.0

    connectivity: float = 1.0

    health: float = 1.0

    constraints: dict[str, float] = field(
        default_factory=dict
    )
