from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class PerfilUsuarioDTO(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefone: Optional[str] = Field(None, min_length=10, max_length=15)


class AlterarSenhaDTO(BaseModel):
    senha_atual: str = Field(..., min_length=1)
    senha_nova: str = Field(..., min_length=8)
    confirmar_senha: str = Field(..., min_length=8)


class AlterarFotoDTO(BaseModel):
    foto: str = Field(..., min_length=1)  # Base64 ou path do arquivo