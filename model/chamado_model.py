from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.enums import ChamadoStatus

@dataclass
class Chamado:
    id_chamado: int
    id_usuario: int
    id_admin: Optional[int]
    titulo: str
    descricao: str
    status: ChamadoStatus
    data: datetime
