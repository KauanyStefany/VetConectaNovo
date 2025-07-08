from dataclasses import dataclass

from model.usuario_model import Usuario

@dataclass
class Veterinario(Usuario):
    crmv: str
    verificado: bool
    bio: str