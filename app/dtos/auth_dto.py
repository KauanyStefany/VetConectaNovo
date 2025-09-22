from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginDTO(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=1)
    redirect: Optional[str] = None


class CadastroDTO(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefone: str = Field(..., min_length=10, max_length=15)
    senha: str = Field(..., min_length=8)
    confirmar_senha: str = Field(..., min_length=8)
    perfil: str = Field(..., regex="^(tutor|veterinario)$")
    crmv: Optional[str] = None


class EsqueciSenhaDTO(BaseModel):
    email: EmailStr


class RedefinirSenhaDTO(BaseModel):
    senha: str = Field(..., min_length=8)
    confirmar_senha: str = Field(..., min_length=8)
    token: str = Field(..., min_length=1)