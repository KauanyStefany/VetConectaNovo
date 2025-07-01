from dataclasses import dataclass
from typing import Optional
from data.administrador_model import Administrador
from data.usuario_model import Usuario

@dataclass
class Denuncia:
    id_denuncia: Optional[int] 
    id_usuario: int
    id_admin: int
    motivo: str
    data_denuncia: str
    status: str
