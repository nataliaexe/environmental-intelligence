from dataclasses import dataclass

from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.intelligence.metrics import (
    active_agents,
    average_energy,
    calculate_connectivity,
    calculate_coverage,
)


@dataclass(frozen=True)
class SwarmHealth:
    active_agents: int
    total_agents: int

    coverage: float
    connectivity: float
    average_energy: float

    health_score: float


def calculate_swarm_health(
    agents: list[SimulatedAgent],
    world_width: float,
    world_height: float,
    connection_radius: float,
    sensing_radius: float = 8.0,
) -> SwarmHealth:

    active = active_agents(agents)

    coverage = calculate_coverage(
        agents=agents,
        world_width=world_width,
        world_height=world_height,
        sensing_radius=sensing_radius,
    )

    connectivity = calculate_connectivity(
        agents=agents,
        connection_radius=connection_radius,
    )

    energy = average_energy(agents)

    survival_ratio = (
        len(active) / len(agents)
        if agents
        else 0.0
    )

    normalized_energy = energy / 100.0

    health = (
        coverage * 0.25
        + connectivity * 0.30
        + normalized_energy * 0.20
        + survival_ratio * 0.25
    )

    return SwarmHealth(
        active_agents=len(active),
        total_agents=len(agents),
        coverage=coverage,
        connectivity=connectivity,
        average_energy=energy,
        health_score=round(
            min(max(health, 0.0), 1.0),
            4,
        ),
    )
