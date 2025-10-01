"""
DTOs relacionados a usuários.
Agrupa todas as validações e estruturas de dados para operações com usuários.
"""

from pydantic import EmailStr, Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_cpf, validar_telefone
)


class CriarUsuarioDTO(BaseDTO):
    """
    DTO para criação de novo usuário.
    Usado em formulários de registro.
    """

    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nome completo do usuário"
    )
    email: EmailStr = Field(
        ...,
        description="E-mail válido do usuário"
    )
    telefone: str = Field(
        ...,
        min_length=10,
        description="Telefone com DDD"
    )
    cpf: Optional[str] = Field(
        None,
        description="CPF (opcional)"
    )

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

    @field_validator('cpf')
    @classmethod
    def validar_cpf_campo(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf(valor),
            "CPF"
        )
        return validador(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "João Silva",
            "email": "joao.silva@email.com",
            "telefone": "(11) 99999-9999",
            "cpf": "123.456.789-01"
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarUsuarioDTO(BaseDTO):
    """
    DTO para atualização de dados do usuário.
    Campos opcionais para atualização parcial.
    """

    nome: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nome completo"
    )
    telefone: Optional[str] = Field(
        None,
        description="Telefone"
    )

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

    @field_validator('telefone')
    @classmethod
    def validar_telefone_campo(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)


# Configurar exemplos JSON nos model_config
CriarUsuarioDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarUsuarioDTO.criar_exemplo_json()
    }
})