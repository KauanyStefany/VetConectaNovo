from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from app.models.enums import DenunciaStatus


@dataclass
class Denuncia:
    id_denuncia: Optional[int]
    id_usuario: int
    id_admin: int
    motivo: str
    data_denuncia: datetime
    status: DenunciaStatus
