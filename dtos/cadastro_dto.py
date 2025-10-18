"""
DTOs para cadastro de usuários (tutor e veterinário).
Implementa validações robustas usando funções centralizadas.
"""

from pydantic import EmailStr, Field, field_validator, model_validator
from typing import Literal
from .base_dto import BaseDTO
from util.validacoes_dto import (
    validar_nome_pessoa,
    validar_telefone,
    validar_crmv,
    validar_senha,
    validar_senhas_coincidem,
    ValidacaoError
)


class CadastroBaseDTO(BaseDTO):
    """DTO base para cadastro de usuários"""

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
        description="Telefone com DDD (10 ou 11 dígitos)"
    )

    senha: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Senha do usuário",
        exclude=True  # Excluir de serialização por segurança
    )

    confirmar_senha: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Confirmação da senha",
        exclude=True  # Excluir de serialização por segurança
    )

    perfil: Literal["tutor", "veterinario"] = Field(
        ...,
        description="Tipo de perfil do usuário"
    )

    # Validadores de campo
    @field_validator('nome')
    @classmethod
    def validar_nome_campo(cls, v: str) -> str:
        """Valida nome completo usando função centralizada"""
        validador = cls.validar_campo_wrapper(validar_nome_pessoa, "Nome")
        return validador(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone_campo(cls, v: str) -> str:
        """Valida telefone usando função centralizada"""
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)

    @field_validator('senha')
    @classmethod
    def validar_senha_campo(cls, v: str) -> str:
        """Valida senha usando função centralizada"""
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(
                valor, min_chars=8, max_chars=128, obrigatorio=True
            ),
            "Senha"
        )
        return validador(v)

    # Validador de modelo
    @model_validator(mode='after')
    def validar_senhas_coincidem_model(self):
        """Valida se as senhas coincidem"""
        try:
            validar_senhas_coincidem(self.senha, self.confirmar_senha)
        except ValidacaoError as e:
            raise ValueError(str(e))
        return self

    def to_dict_safe(self) -> dict:
        """Retorna dados sem campos sensíveis (senhas)"""
        data = self.to_dict()
        data.pop('senha', None)
        data.pop('confirmar_senha', None)
        return data


class CadastroTutorDTO(CadastroBaseDTO):
    """DTO para cadastro de tutor"""

    perfil: Literal["tutor", "veterinario"] = Field(
        default="tutor",
        description="Perfil fixo como tutor"
    )

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Cria exemplo JSON para documentação"""
        return {
            "nome": "João Silva Santos",
            "email": "joao@example.com",
            "telefone": "27999887766",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "perfil": "tutor",
            **overrides
        }


class CadastroVeterinarioDTO(CadastroBaseDTO):
    """DTO para cadastro de veterinário"""

    perfil: Literal["tutor", "veterinario"] = Field(
        default="veterinario",
        description="Perfil fixo como veterinário"
    )

    crmv: str = Field(
        ...,
        min_length=6,
        max_length=10,
        description="CRMV do veterinário (6 dígitos)"
    )

    @field_validator('crmv')
    @classmethod
    def validar_crmv_campo(cls, v: str) -> str:
        """Validação de CRMV - obrigatório para veterinários"""
        if not v or not v.strip():
            raise ValueError("CRMV é obrigatório para veterinários")

        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_crmv(valor),
            "CRMV"
        )
        resultado = validador(v)

        if not resultado:
            raise ValueError("CRMV inválido")

        return resultado

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Cria exemplo JSON para documentação"""
        return {
            "nome": "Dra. Maria Silva",
            "email": "maria@example.com",
            "telefone": "27999887766",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "perfil": "veterinario",
            "crmv": "123456",
            **overrides
        }
