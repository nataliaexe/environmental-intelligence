from app.services.fusion.kalman import (
    ScalarKalmanFilter,
)
from app.services.fusion.result import (
    FusedValue,
)


class SensorFusionEngine:

    def __init__(
        self,
        initial_estimate: float = 0.0,
    ) -> None:

        self.filters: dict[
            str,
            ScalarKalmanFilter,
        ] = {}

        self.sources: dict[
            str,
            set[str],
        ] = {}

        self.initial_estimate = (
            initial_estimate
        )

    def update(
        self,
        variable: str,
        value: float,
        source: str,
        variance: float,
        process_variance: float = 0.01,
    ) -> FusedValue:

        if variable not in self.filters:
            self.filters[variable] = (
                ScalarKalmanFilter(
                    estimate=self.initial_estimate,
                    variance=variance,
                    process_variance=process_variance,
                    measurement_variance=variance,
                )
            )

            self.sources[variable] = set()

        estimate = self.filters[
            variable
        ].update(
            measurement=value,
            measurement_variance=variance,
        )

        self.sources[
            variable
        ].add(source)

        posterior_variance = (
            self.filters[variable].variance
        )

        confidence = 1.0 / (
            1.0 + posterior_variance
        )

        return FusedValue(
            variable=variable,
            value=estimate,
            variance=posterior_variance,
            confidence=confidence,
            sources=tuple(
                sorted(
                    self.sources[variable]
                )
            ),
        )


sensor_fusion = SensorFusionEngine()
