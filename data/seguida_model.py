from dataclasses import dataclass
from datetime import date
from typing import Optional

from data.tutor_model import Tutor
from data.veterinario_model import Veterinario

@dataclass
class Seguida:
    id_veterinario: int
    id_tutor: int
    data_inicio: date
    veterinario: Optional[Veterinario] = None
    tutor: Optional[Tutor] = None