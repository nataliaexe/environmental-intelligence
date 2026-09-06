from app.domain.agent import EnvironmentalAgent
from app.domain.mission import Mission
from app.domain.mission_state import MissionState
from app.domain.authorization import AuthorizationStatus

from app.services.agents.coordinator import swarm_coordinator
from app.services.agents.matching import agent_matcher
from app.services.agents.tasks import task_service

from app.services.missions.lifecycle import mission_lifecycle

from app.services.missions.planner import mission_planner
from app.services.missions.orchestration import (
    OrchestrationResult,
)

from app.services.safety.evaluator import mission_evaluator


class MissionOrchestrator:

    def create_plan(
        self,
        mission: Mission,
    ) -> Mission:

        mission_planner.plan(
            mission
        )

        mission_lifecycle.transition(
            mission,
            MissionState.PLANNED,
            "mission_plan_created",
        )

        return mission

    def authorize(
        self,
        mission: Mission,
        agents: list[EnvironmentalAgent],
        hazard_id: str,
        risk_score: float,
    ) -> list:

        matches = agent_matcher.match(
            mission=mission,
            agents=agents,
        )

        decisions = []

        for match in matches:

            agent = next(
                (
                    agent
                    for agent in agents
                    if agent.id == match.agent_id
                ),
                None,
            )

            if agent is None:
                continue

            evaluation = mission_evaluator.evaluate(
                mission=mission,
                agent=agent,
                hazard_id=hazard_id,
                risk_score=risk_score,
            )

            decisions.append(
                evaluation.decision
            )

        return decisions

    def assign(
        self,
        mission: Mission,
        agents: list[EnvironmentalAgent],
        minimum_agents: int,
        authorization_decisions: list | None = None,
    ):

        if authorization_decisions is not None:

            if any(
                decision.status
                != AuthorizationStatus.AUTHORIZED
                for decision in authorization_decisions
            ):
                mission_lifecycle.transition(
                    mission,
                    MissionState.BLOCKED,
                    "safety_authorization_not_granted",
                )

                return None

        assignment = swarm_coordinator.assign(
            mission=mission,
            agents=agents,
            minimum_agents=minimum_agents,
        )

        if assignment is None:

            mission_lifecycle.transition(
                mission,
                MissionState.BLOCKED,
                "insufficient_compatible_agents",
            )

            return None

        mission_lifecycle.transition(
            mission,
            MissionState.ASSIGNED,
            "swarm_assigned",
        )

        return assignment

    def execute(
        self,
        mission: Mission,
        agents: list[EnvironmentalAgent],
    ) -> list:

        tasks = task_service.create_tasks(
            mission=mission,
            agents=agents,
        )

        if not tasks:

            mission_lifecycle.transition(
                mission,
                MissionState.FAILED,
                "no_tasks_created",
            )

            return []

        mission_lifecycle.transition(
            mission,
            MissionState.EXECUTING,
            "tasks_created",
        )

        for task in tasks:

            agent = next(
                (
                    agent
                    for agent in agents
                    if agent.id == task.agent_id
                ),
                None,
            )

            if agent is None:
                continue

            task_service.start_task(
                task=task,
                agent=agent,
            )

        return tasks

    def verify(
        self,
        mission: Mission,
        success: bool,
        confidence: float,
        evidence: list[str],
    ):

        mission_lifecycle.transition(
            mission,
            MissionState.OBSERVING,
            "observations_received",
        )

        mission_lifecycle.transition(
            mission,
            MissionState.VERIFYING,
            "verification_started",
        )

        from app.services.missions.verification import (
            mission_verification,
        )

        result = mission_verification.verify(
            mission=mission,
            success=success,
            confidence=confidence,
            evidence=evidence,
        )

        if result.success and result.confidence >= 0.7:

            mission_lifecycle.transition(
                mission,
                MissionState.COMPLETED,
                "mission_verified",
            )

        else:

            mission_lifecycle.transition(
                mission,
                MissionState.EXECUTING,
                "verification_insufficient",
            )

        return result


mission_orchestrator = MissionOrchestrator()
