from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.vector import Vector2


def alignment(
    agent: SimulatedAgent,
    neighbors: list[SimulatedAgent],
) -> Vector2:
    if not neighbors:
        return Vector2()

    average_velocity = Vector2()

    for neighbor in neighbors:
        average_velocity += neighbor.velocity

    average_velocity *= 1.0 / len(neighbors)

    return average_velocity - agent.velocity
