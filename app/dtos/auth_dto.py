from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class LoginDto(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=1)
    redirect: Optional[str] = None


class CadastroTutorDto(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefone: str = Field(..., min_length=10, max_length=15)
    cpf: str = Field(..., min_length=11, max_length=14)
    senha: str = Field(..., min_length=8)
    confirmar_senha: str = Field(..., min_length=8)

    @validator('confirmar_senha')
    def senhas_conferem(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('As senhas não coincidem')
        return v


class CadastroVeterinarioDto(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefone: str = Field(..., min_length=10, max_length=15)
    crmv: str = Field(..., min_length=5)
    especialidade: Optional[str] = Field(None, max_length=100)
    senha: str = Field(..., min_length=8)
    confirmar_senha: str = Field(..., min_length=8)

    @validator('confirmar_senha')
    def senhas_conferem(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('As senhas não coincidem')
        return v


class EsqueciSenhaDto(BaseModel):
    email: EmailStr


class RedefinirSenhaDto(BaseModel):
    senha: str = Field(..., min_length=8)
    confirmar_senha: str = Field(..., min_length=8)
    token: str = Field(..., min_length=1)

    @validator('confirmar_senha')
    def senhas_conferem(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('As senhas não coincidem')
        return v


class AlterarSenhaDto(BaseModel):
    senha_atual: str = Field(..., min_length=1)
    nova_senha: str = Field(..., min_length=8)
    confirmar_nova_senha: str = Field(..., min_length=8)

    @validator('confirmar_nova_senha')
    def senhas_conferem(cls, v, values):
        if 'nova_senha' in values and v != values['nova_senha']:
            raise ValueError('As senhas não coincidem')
        return v


class AlterarDadosDto(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    telefone: str = Field(..., min_length=10, max_length=15)