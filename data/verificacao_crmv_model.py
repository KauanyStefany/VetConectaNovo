from dataclasses import dataclass
from data.veterinario_model import Veterinario
from data.administrador_model import Administrador

@dataclass
class VerificacaoCRMV:
    id: int
    veterinario: int | Veterinario
    administrador: Administrador
    data_verificacao: str
    status_verificacao: str
