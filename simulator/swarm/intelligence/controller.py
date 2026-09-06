from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.intelligence.engine import (
    SwarmIntelligenceEngine,
)
from simulator.swarm.intelligence.reconfiguration import (
    ReconfigurationDecision,
)
from simulator.swarm.vector import Vector2
from simulator.swarm.world import SwarmWorld


class SwarmController:
    def __init__(
        self,
        intelligence: SwarmIntelligenceEngine | None = None,
    ) -> None:
        self.intelligence = (
            intelligence
            or SwarmIntelligenceEngine()
        )

    def evaluate(
        self,
        agents: list[SimulatedAgent],
        world: SwarmWorld,
        connection_radius: float,
    ) -> ReconfigurationDecision:
        state = self.intelligence.evaluate(
            agents=agents,
            world_width=world.width,
            world_height=world.height,
            connection_radius=connection_radius,
        )

        return state.reconfiguration

    def execute(
        self,
        decision: ReconfigurationDecision,
        agents: list[SimulatedAgent],
        world: SwarmWorld,
    ) -> None:
        if decision.action == "increase_coverage":
            self._increase_coverage(
                agents,
                world,
            )

        elif decision.action == "restore_connectivity":
            self._restore_connectivity(
                agents,
            )

        elif decision.action == "reduce_operational_area":
            self._reduce_operational_area(
                agents,
            )

        elif decision.action == "return_to_safe_state":
            self._return_to_safe_state(
                agents,
                world,
            )

    def _increase_coverage(
        self,
        agents: list[SimulatedAgent],
        world: SwarmWorld,
    ) -> None:
        active = [
            agent
            for agent in agents
            if agent.active
        ]

        if not active:
            return

        columns = max(
            1,
            int(len(active) ** 0.5),
        )

        rows = (
            len(active) + columns - 1
        ) // columns

        spacing_x = world.width / (
            columns + 1
        )

        spacing_y = world.height / (
            rows + 1
        )

        for index, agent in enumerate(active):
            row = index // columns
            column = index % columns

            target_x = (
                spacing_x * (column + 1)
            )

            target_y = (
                spacing_y * (row + 1)
            )

            agent.navigation_target = Vector2(
                target_x,
                target_y,
            )

    def _restore_connectivity(
        self,
        agents: list[SimulatedAgent],
    ) -> None:
        active = [
            agent
            for agent in agents
            if agent.active
        ]

        if len(active) < 2:
            return

        center = Vector2()

        for agent in active:
            center += agent.position

        center *= 1.0 / len(active)

        for agent in active:
            agent.navigation_target = center

    def _reduce_operational_area(
        self,
        agents: list[SimulatedAgent],
    ) -> None:
        active = [
            agent
            for agent in agents
            if agent.active
        ]

        if len(active) < 2:
            return

        center = Vector2()

        for agent in active:
            center += agent.position

        center *= 1.0 / len(active)

        for agent in active:
            agent.navigation_target = center

    def _return_to_safe_state(
        self,
        agents: list[SimulatedAgent],
        world: SwarmWorld,
    ) -> None:
        safe_point = Vector2(
            world.width / 2,
            world.height / 2,
        )

        for agent in agents:
            if not agent.active:
                continue

            agent.navigation_target = safe_point


swarm_controller = SwarmController()
