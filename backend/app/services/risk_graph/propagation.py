from dataclasses import dataclass
from math import exp

from app.services.risk_graph.model import RiskGraph


@dataclass(frozen=True)
class RiskPropagation:
    hazard: str

    propagated_score: float

    path: tuple[str, ...]

    contributing_paths: tuple[tuple[str, ...], ...]


class RiskGraphEngine:

    def propagate(
        self,
        graph: RiskGraph,
        initial_risks: dict[str, float],
        max_depth: int = 3,
    ) -> list[RiskPropagation]:

        aggregated: dict[
            str,
            dict,
        ] = {}

        queue: list[
            tuple[str, float, tuple[str, ...], int]
        ] = [
            (
                hazard,
                score,
                (hazard,),
                0,
            )
            for hazard, score
            in initial_risks.items()
        ]

        while queue:

            current, score, path, depth = queue.pop(0)

            if depth >= max_depth:
                continue

            outgoing = [
                edge
                for edge in graph.edges
                if edge.source == current
            ]

            for edge in outgoing:

                propagated = self._attenuate(
                    score=score,
                    multiplier=(
                        edge.probability_multiplier
                    ),
                )

                propagated = min(
                    propagated,
                    0.999,
                )

                new_path = (
                    *path,
                    edge.target,
                )

                target = edge.target

                if target not in aggregated:
                    aggregated[target] = {
                        "max_score": propagated,
                        "paths": [new_path],
                    }
                else:
                    aggregated[target]["max_score"] = max(
                        aggregated[target]["max_score"],
                        propagated,
                    )

                    if (
                        new_path
                        not in aggregated[target]["paths"]
                    ):
                        aggregated[target]["paths"].append(
                            new_path
                        )

                queue.append(
                    (
                        edge.target,
                        propagated,
                        new_path,
                        depth + 1,
                    )
                )

        results: list[RiskPropagation] = []

        for hazard, data in aggregated.items():
            results.append(
                RiskPropagation(
                    hazard=hazard,
                    propagated_score=round(
                        data["max_score"],
                        4,
                    ),
                    path=data["paths"][0],
                    contributing_paths=tuple(
                        data["paths"]
                    ),
                )
            )

        return results

    @staticmethod
    def _attenuate(
        score: float,
        multiplier: float,
    ) -> float:
        if score <= 0:
            return 0.0

        if score >= 1.0:
            return 1.0

        # Logistic attenuation:
        # preserves differentiation, monotonic,
        # approaches 1.0 asymptotically.
        logit = (
            score / (1.0 - score)
        )

        adjusted = (
            logit * multiplier
        )

        return (
            adjusted / (1.0 + adjusted)
        )


risk_graph_engine = RiskGraphEngine()
