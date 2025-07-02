from dataclasses import dataclass

from data.usuario_model import Usuario

@dataclass
class Veterinario(Usuario):
    crmv: str
    verificado: bool
    bio: str