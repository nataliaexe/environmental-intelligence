from datetime import datetime, timezone

from app.domain.mission import Mission
from app.domain.mission_history import MissionTransition
from app.domain.mission_state import MissionState
from app.services.missions.state_machine import can_transition


class MissionLifecycle:
    def __init__(self) -> None:
        self._history: list[MissionTransition] = []

    def transition(
        self,
        mission: Mission,
        new_state: MissionState,
        reason: str,
    ) -> None:
        previous = mission.status

        if not can_transition(
            previous,
            new_state,
        ):
            raise ValueError(
                f"Invalid mission transition: "
                f"{previous.value} -> "
                f"{new_state.value}"
            )

        mission.status = new_state

        now = datetime.now(timezone.utc)

        if new_state == MissionState.EXECUTING:
            mission.started_at = now

        if new_state == MissionState.COMPLETED:
            mission.completed_at = now

        self._history.append(
            MissionTransition(
                mission_id=mission.id,
                from_state=previous,
                to_state=new_state,
                timestamp=now,
                reason=reason,
            )
        )

    def history(
        self,
        mission_id: str,
    ) -> list[MissionTransition]:
        return [
            transition
            for transition in self._history
            if transition.mission_id == mission_id
        ]


mission_lifecycle = MissionLifecycle()
