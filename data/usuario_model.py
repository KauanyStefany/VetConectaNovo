from dataclasses import dataclass

@dataclass
class Usuario:
    id_usuario: int
    nome: str
    email: str
    senha: str
    telefone: str