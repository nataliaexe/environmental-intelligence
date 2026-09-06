from datetime import datetime, timezone
from uuid import uuid4

from app.domain.agent import AgentState, EnvironmentalAgent
from app.domain.mission import Mission
from app.domain.mission_state import MissionState
from app.domain.task import AgentTask


class AgentTaskService:

    def create_tasks(
        self,
        mission: Mission,
        agents: list[EnvironmentalAgent],
    ) -> list[AgentTask]:
        tasks: list[AgentTask] = []

        for agent_id in mission.assigned_agents:

            agent = next(
                (
                    agent
                    for agent in agents
                    if agent.id == agent_id
                ),
                None,
            )

            if agent is None:
                continue

            task = AgentTask(
                id=f"TASK-{uuid4().hex[:8].upper()}",
                mission_id=mission.id,
                agent_id=agent.id,
                objective=mission.objective,
                created_at=datetime.now(
                    timezone.utc
                ),
            )

            tasks.append(task)

        return tasks

    def start_task(
        self,
        task: AgentTask,
        agent: EnvironmentalAgent,
    ) -> None:
        if task.status != MissionState.ASSIGNED:
            raise ValueError(
                "Only assigned tasks can start."
            )

        task.status = MissionState.EXECUTING

        task.started_at = datetime.now(
            timezone.utc
        )

        agent.state = AgentState.MOVING
        agent.current_mission_id = (
            task.mission_id
        )

    def complete_task(
        self,
        task: AgentTask,
        agent: EnvironmentalAgent,
    ) -> None:
        if task.status != MissionState.EXECUTING:
            raise ValueError(
                "Only executing tasks can complete."
            )

        task.status = MissionState.COMPLETED

        task.completed_at = datetime.now(
            timezone.utc
        )

        agent.state = AgentState.IDLE
        agent.current_mission_id = None


task_service = AgentTaskService()
