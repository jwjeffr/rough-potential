from dataclasses import dataclass
from enum import Enum, auto
from typing import Mapping
from pathlib import Path
import json


@dataclass
class Units(Enum):

    METAL = auto()

    @property
    def boltzmann_constant(self) -> float:
        if self == Units.METAL:
            return 8.617e-5


@dataclass
class Config:

    temperature: float
    colors: Mapping[str, str]
    mean_barrier: float
    units: Units
    num_processes: int

    @property
    def beta(self) -> float:

        assert self.temperature > 0
        return 1.0 / (self.units.boltzmann_constant * self.temperature)

    @classmethod
    def from_json(cls, p: Path):

        with p.open("r") as file:
            dictionary = json.load(file)

        return cls(
            temperature=dictionary["temperature"],
            colors=dictionary["colors"],
            mean_barrier=dictionary["mean_barrier"],
            units=getattr(Units, dictionary["units"]),
            num_processes=dictionary["num_processes"]
        )


CONFIG = Config.from_json(Path("config.json"))
