from dataclasses import dataclass
from math import sqrt


@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, scalar: float) -> "Vector2":
        return Vector2(
            self.x * scalar,
            self.y * scalar,
        )

    def magnitude(self) -> float:
        return sqrt(
            self.x * self.x
            + self.y * self.y
        )

    def normalized(self) -> "Vector2":
        magnitude = self.magnitude()

        if magnitude == 0:
            return Vector2()

        return Vector2(
            self.x / magnitude,
            self.y / magnitude,
        )

    def distance_to(self, other: "Vector2") -> float:
        return (self - other).magnitude()
