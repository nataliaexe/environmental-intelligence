from dataclasses import dataclass


@dataclass
class ObjectiveProgress:
    target_coverage: float = 0.0
    current_coverage: float = 0.0

    target_connectivity: float = 0.0
    current_connectivity: float = 0.0

    progress: float = 0.0

    completed: bool = False
