from dataclasses import dataclass


@dataclass(frozen=True)
class FusedValue:
    variable: str

    value: float

    variance: float

    confidence: float

    sources: tuple[str, ...]
