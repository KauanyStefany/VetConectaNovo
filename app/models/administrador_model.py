from dataclasses import dataclass


@dataclass
class Administrador:
    id_admin: int
    nome: str
    email: str
    senha: str
