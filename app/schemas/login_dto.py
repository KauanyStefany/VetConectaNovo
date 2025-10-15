"""
DTO para autenticação de usuário.
Valida credenciais de acesso (email e senha).
"""

from pydantic import EmailStr, Field, field_validator
from .base_dto import BaseDTO
from util.validacoes_dto import validar_senha


class LoginDTO(BaseDTO):
    """
    DTO para autenticação de usuário.
    Valida credenciais de acesso.
    """

    email: EmailStr = Field(
        ...,
        description="E-mail do usuário",
        examples=["usuario@example.com"]
    )

    senha: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Senha do usuário"
    )

    @field_validator('senha')
    @classmethod
    def validar_senha_campo(cls, v: str) -> str:
        """Validação básica de senha para login"""
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(
                valor, min_chars=6, max_chars=128, obrigatorio=True
            ),
            "Senha"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Cria exemplo JSON para documentação"""
        return {
            "email": "usuario@example.com",
            "senha": "senha123",
            **overrides
        }
