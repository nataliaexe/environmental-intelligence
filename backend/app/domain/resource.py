from dataclasses import dataclass
from enum import Enum


class ResourceType(str, Enum):
    ORGANIC_WASTE = "organic_waste"
    BIOMASS = "biomass"
    SOIL_AMENDMENT = "soil_amendment"
    FOOD_SUBSTRATE = "food_substrate"


@dataclass
class Resource:
    id: str

    resource_type: ResourceType

    region_id: str

    mass_kg: float

    quality: float = 1.0

    moisture: float = 0.0

    contamination: float = 0.0

    available: bool = True
