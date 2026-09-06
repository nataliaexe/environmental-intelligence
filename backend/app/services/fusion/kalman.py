from dataclasses import dataclass


@dataclass
class ScalarKalmanFilter:
    estimate: float

    variance: float

    process_variance: float

    measurement_variance: float

    initialized: bool = False

    def update(
        self,
        measurement: float,
        measurement_variance: float | None = None,
    ) -> float:

        if not self.initialized:
            self.estimate = measurement

            if measurement_variance is not None:
                self.variance = (
                    measurement_variance
                )

            self.initialized = True

            return self.estimate

        self.variance += (
            self.process_variance
        )

        r = (
            measurement_variance
            if measurement_variance is not None
            else self.measurement_variance
        )

        gain = (
            self.variance
            / (self.variance + r)
        )

        self.estimate += (
            gain
            * (measurement - self.estimate)
        )

        self.variance = (
            1.0 - gain
        ) * self.variance

        return self.estimate
