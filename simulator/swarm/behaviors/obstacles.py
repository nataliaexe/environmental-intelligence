from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.vector import Vector2
from simulator.swarm.world import Obstacle


def obstacle_avoidance(
    agent: SimulatedAgent,
    obstacles: list[Obstacle],
) -> Vector2:
    force = Vector2()

    for obstacle in obstacles:
        distance = agent.position.distance_to(
            obstacle.center
        )

        safe_distance = obstacle.radius + 2.0

        if distance == 0 or distance >= safe_distance:
            continue

        direction = (
            agent.position - obstacle.center
        ).normalized()

        strength = 1.0 / max(
            distance,
            0.1,
        )

        force += direction * strength

    return force
