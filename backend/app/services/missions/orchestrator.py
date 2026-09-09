from app.domain.agent import EnvironmentalAgent
from app.domain.authorization import (
    AuthorizationDecision,
    AuthorizationStatus,
)
from app.domain.mission import Mission
from app.domain.mission_state import MissionState

from app.services.agents.coordinator import swarm_coordinator
from app.services.agents.matching import agent_matcher
from app.services.agents.tasks import task_service
from app.services.missions.lifecycle import mission_lifecycle
from app.services.missions.orchestration import OrchestrationResult
from app.services.missions.planner import mission_planner
from app.services.safety.evaluator import mission_evaluator


class MissionOrchestrator:

    def create_plan(
        self,
        mission: Mission,
    ) -> Mission:

        mission_planner.plan(mission)

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
        confidence: float,
    ) -> list[AuthorizationDecision]:

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
                confidence=confidence,
            )

            decisions.append(evaluation.decision)

        return decisions

    def assign(
        self,
        mission: Mission,
        agents: list[EnvironmentalAgent],
        minimum_agents: int,
        authorization_decisions: list[AuthorizationDecision],
    ):

        if not authorization_decisions:
            mission_lifecycle.transition(
                mission,
                MissionState.BLOCKED,
                "missing_authorization_decisions",
            )
            return None

        if all(
            decision.status == AuthorizationStatus.DENIED
            for decision in authorization_decisions
        ):
            mission_lifecycle.transition(
                mission,
                MissionState.BLOCKED,
                "safety_authorization_denied",
            )
            return None

        if any(
            decision.status == AuthorizationStatus.REQUIRES_HUMAN
            for decision in authorization_decisions
        ):
            if mission.status != MissionState.AWAITING_APPROVAL:
                mission_lifecycle.transition(
                    mission,
                    MissionState.AWAITING_APPROVAL,
                    "human_confirmation_required",
                )
            return None

        authorized_decisions = [
            decision
            for decision in authorization_decisions
            if decision.status == AuthorizationStatus.AUTHORIZED
        ]

        if len(authorized_decisions) < minimum_agents:
            mission_lifecycle.transition(
                mission,
                MissionState.BLOCKED,
                "insufficient_authorized_agents",
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

    def approve(
        self,
        mission: Mission,
    ) -> Mission | None:

        if mission.status != MissionState.AWAITING_APPROVAL:
            return None

        mission_lifecycle.transition(
            mission,
            MissionState.AUTHORIZED,
            "human_approval_received",
        )

        return mission

    def execute(
        self,
        mission: Mission,
        agents: list[EnvironmentalAgent],
    ) -> list:

        if mission.status != MissionState.ASSIGNED:
            mission_lifecycle.transition(
                mission,
                MissionState.FAILED,
                "mission_not_assigned",
            )
            return []

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
