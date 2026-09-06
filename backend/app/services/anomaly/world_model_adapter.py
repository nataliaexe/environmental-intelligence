from app.domain.anomaly import AnomalyAssessment

from app.services.anomaly.world_model_input import (
    WorldModelAnomalyInput,
)


class WorldModelAnomalyAdapter:

    def prepare(
        self,
        world: WorldModelAnomalyInput,
    ) -> dict[str, float]:
        """
        Produces anomaly-engine-ready values.

        Confidence and uncertainty are preserved
        by the caller and are not discarded here.
        """

        return dict(world.values)


world_model_anomaly_adapter = (
    WorldModelAnomalyAdapter()
)
