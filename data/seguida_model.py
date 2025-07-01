from dataclasses import dataclass
from datetime import date

from data.tutor_model import Tutor
from data.veterinario_model import Veterinario

@dataclass
class Seguida:
    id_veterinario: Veterinario
    id_tutor: Tutor
    data_inicio: date
# verificar se data_inicio est´CORRETO, verificar se os ints estao corretos