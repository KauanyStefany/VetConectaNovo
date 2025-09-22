from dataclasses import dataclass
from typing import Optional

from app.database.models.usuario_model import Usuario

@dataclass
class Veterinario(Usuario):
    crmv: str
    verificado: bool
    bio: Optional[str]