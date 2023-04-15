from dataclasses import dataclass
from typing import TypeVar

Dummy = TypeVar("Dummy", bound="Dummy")
Action = Dummy
SelectAction = Dummy

@dataclass
class Dummy:
    var: int