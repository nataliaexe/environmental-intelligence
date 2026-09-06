from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.vector import Vector2


def separation(
    agent: SimulatedAgent,
    neighbors: list[SimulatedAgent],
    radius: float,
) -> Vector2:
    force = Vector2()

    for neighbor in neighbors:
        distance = agent.position.distance_to(
            neighbor.position
        )

        if distance == 0 or distance >= radius:
            continue

        direction = (
            agent.position - neighbor.position
        ).normalized()

        strength = 1.0 / distance

        force += direction * strength

    return force
