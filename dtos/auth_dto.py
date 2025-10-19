from pydantic import field_validator, model_validator

from model.enums import PerfilUsuario
from .base_dto import BaseDTO
from util.validacoes_dto import (
    validar_email,
    validar_enum_valor,
    validar_nome_pessoa,
    validar_telefone,
    validar_crmv,
    validar_senha,
    validar_senhas_coincidem,
)


class LoginDTO(BaseDTO):
    email: str
    senha: str

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        return validar_email(v)

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        return validar_senha(v)


class CadastroBaseDTO(BaseDTO):
    nome: str
    email: str
    telefone: str
    senha: str
    confirmar_senha: str
    perfil: str

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        return validar_nome_pessoa(v)

    @field_validator("telefone")
    @classmethod
    def validar_telefone(cls, v: str) -> str:
        return validar_telefone(v)

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        return validar_senha(v, min_chars=8, max_chars=128)

    @field_validator("perfil")
    @classmethod
    def validar_perfil(cls, v: str) -> str:
        return validar_enum_valor(v, PerfilUsuario)

    @model_validator(mode="after")
    def validar_senhas_coincidem_model(self):
        validar_senhas_coincidem(self.senha, self.confirmar_senha)
        return self


class CadastroTutorDTO(CadastroBaseDTO):
    pass


class CadastroVeterinarioDTO(CadastroBaseDTO):
    crmv: str

    @field_validator("crmv")
    @classmethod
    def validar_crmv(cls, v: str) -> str:
        return validar_crmv(v)


class EsqueciSenhaDTO(BaseDTO):
    email: str

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        return validar_email(v)


class RedefinirSenhaDTO(BaseDTO):
    senha: str
    confirmar_senha: str

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        return validar_senha(v, min_chars=8, max_chars=128)

    @model_validator(mode="after")
    def validar_senhas_coincidem_model(self):
        validar_senhas_coincidem(self.senha, self.confirmar_senha)
        return self
