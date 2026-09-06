from dataclasses import dataclass

from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.intelligence.health import (
    SwarmHealth,
    calculate_swarm_health,
)
from simulator.swarm.intelligence.reconfiguration import (
    ReconfigurationDecision,
    decide_reconfiguration,
)


@dataclass(frozen=True)
class SwarmIntelligenceState:
    health: SwarmHealth
    reconfiguration: ReconfigurationDecision


class SwarmIntelligenceEngine:

    def evaluate(
        self,
        agents: list[SimulatedAgent],
        world_width: float,
        world_height: float,
        connection_radius: float,
    ) -> SwarmIntelligenceState:

        health = calculate_swarm_health(
            agents=agents,
            world_width=world_width,
            world_height=world_height,
            connection_radius=connection_radius,
        )

        decision = decide_reconfiguration(
            coverage=health.coverage,
            connectivity=health.connectivity,
            health=health.health_score,
            active_agents=health.active_agents,
            total_agents=health.total_agents,
        )

        return SwarmIntelligenceState(
            health=health,
            reconfiguration=decision,
        )


swarm_intelligence = SwarmIntelligenceEngine()
