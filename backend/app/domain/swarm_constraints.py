from dataclasses import dataclass


@dataclass(frozen=True)
class SwarmConstraints:
    minimum_connectivity: float = 0.8
    minimum_health: float = 0.5
    target_coverage: float = 0.8

    minimum_active_agents: int = 1

    preserve_communication: bool = True
