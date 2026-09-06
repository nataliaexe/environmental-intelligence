from simulator.swarm.vector import Vector2


def target_attraction(
    position: Vector2,
    target: Vector2 | None,
) -> Vector2:
    if target is None:
        return Vector2()

    return target - position
