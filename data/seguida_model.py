from dataclasses import dataclass
from datetime import date
from typing import Optional

from data.tutor_model import Tutor
from data.veterinario_model import Veterinario

@dataclass
class Seguida:
    id_veterinario: Veterinario
    id_tutor: Tutor
    data_inicio: Optional[date] = None