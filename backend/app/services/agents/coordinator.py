from dataclasses import dataclass

from app.domain.agent import AgentState, EnvironmentalAgent
from app.domain.mission import Mission
from app.domain.swarm import Swarm, SwarmObjective
from app.services.agents.formation import choose_formation
from app.services.agents.matching import agent_matcher


@dataclass(frozen=True)
class SwarmAssignment:
    swarm: Swarm
    selected_agents: list[str]


class SwarmCoordinator:
    def assign(
        self,
        mission: Mission,
        agents: list[EnvironmentalAgent],
        minimum_agents: int = 1,
    ) -> SwarmAssignment | None:

        matches = agent_matcher.match(
            mission=mission,
            agents=agents,
        )

        if len(matches) < minimum_agents:
            return None

        selected = [
            match.agent_id
            for match in matches[:minimum_agents]
        ]

        for agent in agents:
            if agent.id in selected:
                agent.state = AgentState.MOVING
                agent.current_mission_id = mission.id

        mission.assigned_agents = selected

        formation = choose_formation(
            objective=mission.objective,
            agent_count=len(selected),
        )

        swarm = Swarm(
            id=f"SWARM-{mission.id}",
            agents=selected,
            objective=SwarmObjective(
                type=mission.objective,
                target_region_id=mission.region_id,
                priority=mission.priority,
                minimum_agents=minimum_agents,
                required_capabilities=list(
                    mission.required_capabilities
                ),
            ),
            formation=formation.value,
            coverage=0.0,
            connectivity=1.0,
            health=1.0,
        )

        return SwarmAssignment(
            swarm=swarm,
            selected_agents=selected,
        )


swarm_coordinator = SwarmCoordinator()
