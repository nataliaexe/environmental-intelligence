from dataclasses import dataclass


@dataclass
class BioreactorState:
    id: str

    capacity_kg: float

    current_mass_kg: float = 0.0

    enzyme_capacity_kg: float = 0.0

    conversion_efficiency: float = 0.0

    protein_output_kg: float = 0.0

    carbohydrate_output_kg: float = 0.0

    lipid_output_kg: float = 0.0

    residual_mass_kg: float = 0.0

    active: bool = False
