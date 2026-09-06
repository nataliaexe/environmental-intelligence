from dataclasses import dataclass

from app.services.risk_graph.model import RiskGraph


@dataclass(frozen=True)
class RiskPropagation:
    hazard: str

    propagated_score: float

    path: tuple[str, ...]


class RiskGraphEngine:

    def propagate(
        self,
        graph: RiskGraph,
        initial_risks: dict[str, float],
        max_depth: int = 3,
    ) -> list[RiskPropagation]:

        results: list[RiskPropagation] = []

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

                propagated = (
                    score
                    * edge.probability_multiplier
                )

                propagated = min(
                    propagated,
                    1.0,
                )

                new_path = (
                    *path,
                    edge.target,
                )

                results.append(
                    RiskPropagation(
                        hazard=edge.target,
                        propagated_score=round(
                            propagated,
                            4,
                        ),
                        path=new_path,
                    )
                )

                queue.append(
                    (
                        edge.target,
                        propagated,
                        new_path,
                        depth + 1,
                    )
                )

        return results


risk_graph_engine = RiskGraphEngine()
