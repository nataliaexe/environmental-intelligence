from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.vector import Vector2


def cohesion(
    agent: SimulatedAgent,
    neighbors: list[SimulatedAgent],
) -> Vector2:
    if not neighbors:
        return Vector2()

    center = Vector2()

    for neighbor in neighbors:
        center += neighbor.position

    center *= 1.0 / len(neighbors)

    return center - agent.position
