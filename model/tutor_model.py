from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Tutor(Usuario):
    quantidade_pets: int = 0
    descricao_pets: Optional[str] = None