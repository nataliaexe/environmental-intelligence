from dataclasses import dataclass


@dataclass(frozen=True)
class FaultInjectionConfig:
    sensor_noise_gaussian_std: float = 0.0

    packet_loss_rate: float = 0.0

    actuator_lag_seconds: float = 0.0

    sensor_failure_rate: float = 0.0

    agent_failure_rate: float = 0.0


@dataclass(frozen=True)
class SwarmConfig:
    neighbor_radius: float = 8.0
    separation_radius: float = 2.0

    separation_weight: float = 1.8
    alignment_weight: float = 1.0
    cohesion_weight: float = 0.8
    target_weight: float = 1.2
    obstacle_weight: float = 2.0

    max_speed: float = 1.0
    max_acceleration: float = 0.1

    energy_per_step: float = 0.02

    fault_injection: FaultInjectionConfig = (
        FaultInjectionConfig()
    )
