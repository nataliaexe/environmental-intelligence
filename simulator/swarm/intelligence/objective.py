from simulator.swarm.intelligence.objective_state import (
    ObjectiveProgress,
)


def evaluate_objective(
    coverage: float,
    connectivity: float,
    target_coverage: float,
    target_connectivity: float,
) -> ObjectiveProgress:

    coverage_progress = (
        min(
            coverage / target_coverage,
            1.0,
        )
        if target_coverage > 0
        else 1.0
    )

    connectivity_progress = (
        min(
            connectivity / target_connectivity,
            1.0,
        )
        if target_connectivity > 0
        else 1.0
    )

    progress = (
        coverage_progress * 0.6
        + connectivity_progress * 0.4
    )

    completed = (
        coverage >= target_coverage
        and connectivity >= target_connectivity
    )

    return ObjectiveProgress(
        target_coverage=target_coverage,
        current_coverage=coverage,
        target_connectivity=target_connectivity,
        current_connectivity=connectivity,
        progress=round(progress, 4),
        completed=completed,
    )
