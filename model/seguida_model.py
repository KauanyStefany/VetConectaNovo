from dataclasses import dataclass
from datetime import date


@dataclass
class Seguida:
    id_seguidor: int
    id_seguido: int
    data_inicio: date
