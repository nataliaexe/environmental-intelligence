from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyConstraints:
    maximum_speed: float = 1.0

    minimum_battery_for_mission: float = 20.0

    maximum_environmental_risk: float = 0.8

    allow_unknown_terrain: bool = False

    allow_autonomous_actuation: bool = False
