from dataclasses import dataclass, field
from enum import Enum


class HazardDomain(str, Enum):
    HYDROMETEOROLOGICAL = "hydrometeorological"
    GEOLOGICAL = "geological"
    ENVIRONMENTAL = "environmental"
    CHEMICAL = "chemical"
    BIOLOGICAL = "biological"
    TECHNOLOGICAL = "technological"
    EXTRATERRESTRIAL = "extraterrestrial"
    SOCIETAL = "societal"


@dataclass(frozen=True)
class HazardDefinition:
    id: str
    name: str
    domain: HazardDomain

    description: str

    required_observations: list[str] = field(
        default_factory=list
    )

    compatible_capabilities: list[str] = field(
        default_factory=list
    )

    possible_actions: list[str] = field(
        default_factory=list
    )
