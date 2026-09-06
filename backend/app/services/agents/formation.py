from app.domain.formation import FormationType


def choose_formation(
    objective: str,
    agent_count: int,
) -> FormationType:
    if objective == "investigate_wildfire":
        return FormationType.CONVERGED

    if objective == "increase_sensor_density":
        return FormationType.GRID

    if objective == "increase_coverage":
        return FormationType.DISTRIBUTED

    if objective == "create_monitoring_barrier":
        return FormationType.LINE

    if objective == "communication_relay":
        return FormationType.RELAY

    if agent_count >= 6:
        return FormationType.GRID

    return FormationType.DISTRIBUTED
