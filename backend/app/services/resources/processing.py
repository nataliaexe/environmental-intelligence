from dataclasses import dataclass

from app.domain.bioreactor import BioreactorState
from app.domain.resource import Resource, ResourceType


@dataclass(frozen=True)
class ProcessingResult:
    input_mass_kg: float

    accepted_mass_kg: float

    rejected_mass_kg: float

    protein_kg: float
    carbohydrate_kg: float
    lipid_kg: float

    residual_kg: float

    success: bool


class BiomassProcessor:

    def process(
        self,
        reactor: BioreactorState,
        resource: Resource,
    ) -> ProcessingResult:

        if resource.resource_type != ResourceType.ORGANIC_WASTE:
            return ProcessingResult(
                input_mass_kg=resource.mass_kg,
                accepted_mass_kg=0.0,
                rejected_mass_kg=resource.mass_kg,
                protein_kg=0.0,
                carbohydrate_kg=0.0,
                lipid_kg=0.0,
                residual_kg=0.0,
                success=False,
            )

        if not resource.available:
            return ProcessingResult(
                input_mass_kg=resource.mass_kg,
                accepted_mass_kg=0.0,
                rejected_mass_kg=resource.mass_kg,
                protein_kg=0.0,
                carbohydrate_kg=0.0,
                lipid_kg=0.0,
                residual_kg=0.0,
                success=False,
            )

        remaining_capacity = max(
            0.0,
            reactor.capacity_kg
            - reactor.current_mass_kg,
        )

        accepted_mass = min(
            resource.mass_kg,
            remaining_capacity,
        )

        rejected_mass = (
            resource.mass_kg
            - accepted_mass
        )

        if accepted_mass <= 0:
            return ProcessingResult(
                input_mass_kg=resource.mass_kg,
                accepted_mass_kg=0.0,
                rejected_mass_kg=resource.mass_kg,
                protein_kg=0.0,
                carbohydrate_kg=0.0,
                lipid_kg=0.0,
                residual_kg=0.0,
                success=False,
            )

        usable_fraction = (
            resource.quality
            * (1.0 - resource.contamination)
        )

        usable_fraction = max(
            0.0,
            min(usable_fraction, 1.0),
        )

        usable_mass = (
            accepted_mass
            * usable_fraction
            * max(
                0.0,
                min(
                    reactor.conversion_efficiency,
                    1.0,
                ),
            )
        )

        protein = usable_mass * 0.35
        carbohydrate = usable_mass * 0.35
        lipid = usable_mass * 0.15

        residual = (
            accepted_mass
            - protein
            - carbohydrate
            - lipid
        )

        reactor.current_mass_kg += accepted_mass

        reactor.protein_output_kg += protein
        reactor.carbohydrate_output_kg += carbohydrate
        reactor.lipid_output_kg += lipid
        reactor.residual_mass_kg += residual

        resource.available = False

        return ProcessingResult(
            input_mass_kg=resource.mass_kg,
            accepted_mass_kg=accepted_mass,
            rejected_mass_kg=rejected_mass,
            protein_kg=round(protein, 4),
            carbohydrate_kg=round(
                carbohydrate,
                4,
            ),
            lipid_kg=round(
                lipid,
                4,
            ),
            residual_kg=round(
                residual,
                4,
            ),
            success=True,
        )


biomass_processor = BiomassProcessor()
