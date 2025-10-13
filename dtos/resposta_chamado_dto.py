from pydantic import BaseModel, field_validator
from typing import Optional

class RespostaChamadoDTO(BaseModel):
    id_chamado: int
    titulo: str
    descricao: str
    data: Optional[str] = None  # data pode ser preenchida automaticamente

    @field_validator('id_chamado')
    @classmethod
    def validate_id_chamado(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError('ID do chamado é obrigatório e deve ser positivo')
        return v

    @field_validator('titulo')
    @classmethod
    def validate_titulo(cls, v):
        if not v or not v.strip():
            raise ValueError('Título é obrigatório')
        if len(v.split()) < 5:
            raise ValueError('Título deve ter pelo menos 5 caracteres')
        if len(v.strip()) > 80:
            raise ValueError('Título deve ter no máximo 80 caracteres')
        return v

    @field_validator('descricao')
    @classmethod
    def validate_descricao(cls, v):
        if not v or not v.strip():
            raise ValueError('Descrição é obrigatória')
        if len(v.split()) < 10:
            raise ValueError('Descrição deve ter pelo menos 10 palavras')
        if len(v.strip()) > 500:
            raise ValueError('Descrição deve ter no máximo 500 caracteres')
        return v