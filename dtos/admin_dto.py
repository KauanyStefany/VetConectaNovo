from pydantic import field_validator
from typing import Optional
from .base_dto import BaseDTO
from util.validacoes_dto import validar_texto_obrigatorio

class CriarAdminDTO(BaseDTO):
    """
    DTO para criação de novo administrador.
    Usado em formulários de registro de admin.
    """

    nome: str
    email: str
    senha: str

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Nome"
        )
        return validador(v)

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Senha é obrigatória')
        if len(v.strip()) != 8:
            raise ValueError('Senha deve ter exatamente 8 caracteres')
        return v

class AtualizarAdminDTO(BaseDTO):
    """
    DTO para atualização de dados do administrador.
    Campos opcionais para atualização parcial.
    """

    nome: str
    senha: str

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Nome"
        )
        return validador(v)

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        if len(v.strip()) != 8:
            raise ValueError('Senha deve ter exatamente 8 caracteres')
        return v
