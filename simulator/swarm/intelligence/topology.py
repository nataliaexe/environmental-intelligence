from simulator.swarm.agent_state import SimulatedAgent


def connected_components(
    agents: list[SimulatedAgent],
    connection_radius: float,
) -> list[list[str]]:
    active = [
        agent
        for agent in agents
        if agent.active
    ]

    visited: set[str] = set()
    components: list[list[str]] = []

    for start in active:
        if start.agent_id in visited:
            continue

        component: list[str] = []
        stack = [start]

        while stack:
            current = stack.pop()

            if current.agent_id in visited:
                continue

            visited.add(current.agent_id)
            component.append(current.agent_id)

            for neighbor in active:
                if neighbor.agent_id in visited:
                    continue

                distance = current.position.distance_to(
                    neighbor.position
                )

                if distance <= connection_radius:
                    stack.append(neighbor)

        components.append(component)

    return components


def is_fully_connected(
    agents: list[SimulatedAgent],
    connection_radius: float,
) -> bool:
    components = connected_components(
        agents,
        connection_radius,
    )

    return len(components) <= 1
