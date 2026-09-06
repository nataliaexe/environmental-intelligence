from dataclasses import dataclass, field


@dataclass
class VectorClock:
    values: dict[str, int] = field(
        default_factory=dict
    )

    def increment(
        self,
        node_id: str,
    ) -> None:
        self.values[node_id] = (
            self.values.get(node_id, 0) + 1
        )

    def update(
        self,
        other: "VectorClock",
    ) -> None:
        for node_id, value in other.values.items():
            self.values[node_id] = max(
                self.values.get(node_id, 0),
                value,
            )

    def copy(self) -> "VectorClock":
        return VectorClock(
            values=dict(self.values)
        )


def happens_before(
    left: VectorClock,
    right: VectorClock,
) -> bool:
    keys = (
        set(left.values)
        | set(right.values)
    )

    less_or_equal = all(
        left.values.get(key, 0)
        <= right.values.get(key, 0)
        for key in keys
    )

    strictly_less = any(
        left.values.get(key, 0)
        < right.values.get(key, 0)
        for key in keys
    )

    return less_or_equal and strictly_less


def concurrent(
    left: VectorClock,
    right: VectorClock,
) -> bool:
    return not (
        happens_before(left, right)
        or happens_before(right, left)
        or left.values == right.values
    )
