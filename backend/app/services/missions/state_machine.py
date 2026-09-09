from app.domain.mission_state import MissionState


ALLOWED_TRANSITIONS: dict[
    MissionState,
    set[MissionState],
] = {
    MissionState.PENDING: {
        MissionState.PLANNED,
        MissionState.CANCELLED,
    },

    MissionState.PLANNED: {
        MissionState.AUTHORIZED,
        MissionState.AWAITING_APPROVAL,
        MissionState.BLOCKED,
        MissionState.CANCELLED,
    },

    MissionState.AWAITING_APPROVAL: {
        MissionState.AUTHORIZED,
        MissionState.BLOCKED,
        MissionState.CANCELLED,
    },

    MissionState.AUTHORIZED: {
        MissionState.ASSIGNED,
        MissionState.BLOCKED,
        MissionState.CANCELLED,
    },

    MissionState.ASSIGNED: {
        MissionState.EXECUTING,
        MissionState.BLOCKED,
        MissionState.CANCELLED,
    },

    MissionState.EXECUTING: {
        MissionState.OBSERVING,
        MissionState.FAILED,
        MissionState.CANCELLED,
    },

    MissionState.OBSERVING: {
        MissionState.VERIFYING,
        MissionState.FAILED,
    },

    MissionState.VERIFYING: {
        MissionState.COMPLETED,
        MissionState.EXECUTING,
        MissionState.FAILED,
    },

    MissionState.COMPLETED: set(),

    MissionState.FAILED: set(),

    MissionState.BLOCKED: {
        MissionState.PLANNED,
        MissionState.CANCELLED,
    },

    MissionState.CANCELLED: set(),
}


def can_transition(
    current: MissionState,
    target: MissionState,
) -> bool:
    return target in ALLOWED_TRANSITIONS.get(
        current,
        set(),
    )
