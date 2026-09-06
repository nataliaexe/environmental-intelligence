from dataclasses import dataclass


@dataclass
class ResourceNode:
    id: str

    region_id: str

    x: float
    y: float

    resource_type: str

    available_mass_kg: float

    quality: float = 1.0

    contamination: float = 0.0
