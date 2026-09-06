from math import sqrt

from simulator.swarm.agent_state import SimulatedAgent


def active_agents(
    agents: list[SimulatedAgent],
) -> list[SimulatedAgent]:
    return [
        agent
        for agent in agents
        if agent.active
    ]


def calculate_coverage(
    agents: list[SimulatedAgent],
    world_width: float,
    world_height: float,
    sensing_radius: float = 8.0,
    grid_resolution: int = 20,
) -> float:
    active = active_agents(agents)

    if not active:
        return 0.0

    covered_cells = 0
    total_cells = (
        grid_resolution
        * grid_resolution
    )

    cell_width = (
        world_width
        / grid_resolution
    )

    cell_height = (
        world_height
        / grid_resolution
    )

    for x in range(grid_resolution):
        for y in range(grid_resolution):
            point_x = (
                x + 0.5
            ) * cell_width

            point_y = (
                y + 0.5
            ) * cell_height

            observed = any(
                sqrt(
                    (
                        agent.position.x
                        - point_x
                    ) ** 2
                    +
                    (
                        agent.position.y
                        - point_y
                    ) ** 2
                )
                <= sensing_radius
                for agent in active
            )

            if observed:
                covered_cells += 1

    return round(
        covered_cells / total_cells,
        4,
    )


def calculate_connectivity(
    agents: list[SimulatedAgent],
    connection_radius: float,
) -> float:
    active = active_agents(agents)

    if len(active) <= 1:
        return 1.0 if active else 0.0

    connected = 0

    for agent in active:
        has_neighbor = any(
            agent is not other
            and agent.position.distance_to(
                other.position
            ) <= connection_radius
            for other in active
        )

        if has_neighbor:
            connected += 1

    return round(
        connected / len(active),
        4,
    )


def average_energy(
    agents: list[SimulatedAgent],
) -> float:
    active = active_agents(agents)

    if not active:
        return 0.0

    return round(
        sum(
            agent.energy
            for agent in active
        ) / len(active),
        4,
    )


def average_distance_from_center(
    agents: list[SimulatedAgent],
    world_width: float,
    world_height: float,
) -> float:
    active = active_agents(agents)

    if not active:
        return 0.0

    center_x = world_width / 2
    center_y = world_height / 2

    distances = [
        sqrt(
            (
                agent.position.x
                - center_x
            ) ** 2
            +
            (
                agent.position.y
                - center_y
            ) ** 2
        )
        for agent in active
    ]

    return round(
        sum(distances)
        / len(distances),
        4,
    )
