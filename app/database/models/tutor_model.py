from dataclasses import dataclass
from typing import Optional

from app.database.models.usuario_model import Usuario

@dataclass
class Tutor(Usuario):
    quantidade_pets: int
    descricao_pets: Optional[str]