from dataclasses import dataclass
from datetime import datetime

from app.models.enums import ChamadoStatus


@dataclass
class Chamado:
    id_chamado: int
    id_usuario: int
    id_admin: int
    titulo: str
    descricao: str
    status: ChamadoStatus
    data: datetime
