from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id_usuario: int
    nome: str
    email: str
    senha: str
    telefone: str
    perfil: str
    token_redefinicao: Optional[str]
    data_token: Optional[str]
    data_cadastro: Optional[str]