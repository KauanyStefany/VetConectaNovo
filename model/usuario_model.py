from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id_usuario: int
    nome: str
    email: str
    senha: str
    telefone: str
    perfil: str = 'cliente'
    foto: Optional[str] = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None