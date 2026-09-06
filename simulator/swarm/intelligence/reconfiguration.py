from dataclasses import dataclass


@dataclass(frozen=True)
class ReconfigurationDecision:
    action: str
    reason: str
    urgency: float


def decide_reconfiguration(
    coverage: float,
    connectivity: float,
    health: float,
    active_agents: int,
    total_agents: int,
) -> ReconfigurationDecision:

    survival_ratio = (
        active_agents / total_agents
        if total_agents
        else 0.0
    )

    if connectivity < 0.5:
        return ReconfigurationDecision(
            action="restore_connectivity",
            reason="swarm_topology_is_fragmented",
            urgency=0.95,
        )

    if survival_ratio < 0.6:
        return ReconfigurationDecision(
            action="reduce_operational_area",
            reason="too_many_agents_unavailable",
            urgency=0.90,
        )

    if coverage < 0.3:
        return ReconfigurationDecision(
            action="increase_coverage",
            reason="environmental_coverage_too_low",
            urgency=0.70,
        )

    if health < 0.5:
        return ReconfigurationDecision(
            action="return_to_safe_state",
            reason="swarm_health_critical",
            urgency=0.85,
        )

    return ReconfigurationDecision(
        action="maintain",
        reason="swarm_operating_normally",
        urgency=0.0,
    )
