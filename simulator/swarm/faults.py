import random

from simulator.swarm.config import FaultInjectionConfig


class FaultInjector:

    def __init__(
        self,
        config: FaultInjectionConfig,
        seed: int | None = None,
    ) -> None:
        self.config = config
        self.random = random.Random(seed)

    def packet_delivered(self) -> bool:
        return (
            self.random.random()
            >= self.config.packet_loss_rate
        )

    def sensor_operational(self) -> bool:
        return (
            self.random.random()
            >= self.config.sensor_failure_rate
        )

    def agent_operational(self) -> bool:
        return (
            self.random.random()
            >= self.config.agent_failure_rate
        )

    def noise(
        self,
        value: float,
    ) -> float:
        std = (
            self.config.sensor_noise_gaussian_std
        )

        if std <= 0:
            return value

        return value + self.random.gauss(
            0.0,
            std,
        )


fault_injector_factory = FaultInjector
