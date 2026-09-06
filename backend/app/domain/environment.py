from dataclasses import dataclass, field

from app.domain.agent import EnvironmentalAgent
from app.domain.region import Region
from app.domain.sensor import Sensor


@dataclass
class Environment:
    id: str
    name: str

    regions: list[Region] = field(default_factory=list)
    sensors: list[Sensor] = field(default_factory=list)
    agents: list[EnvironmentalAgent] = field(default_factory=list)
