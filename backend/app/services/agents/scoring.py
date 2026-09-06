from math import sqrt

from app.domain.agent import EnvironmentalAgent


def distance_to_target(
    agent: EnvironmentalAgent,
    target_x: float,
    target_y: float,
) -> float:
    dx = agent.localization.x - target_x
    dy = agent.localization.y - target_y

    return sqrt(
        dx * dx + dy * dy
    )


def mission_score(
    agent: EnvironmentalAgent,
    target_x: float,
    target_y: float,
) -> float:
    distance = distance_to_target(
        agent=agent,
        target_x=target_x,
        target_y=target_y,
    )

    distance_score = 1.0 / (1.0 + distance)

    energy_score = agent.energy.level / 100.0

    trust_score = agent.trust_score

    return round(
        distance_score * 0.4
        + energy_score * 0.3
        + trust_score * 0.3,
        4,
    )
