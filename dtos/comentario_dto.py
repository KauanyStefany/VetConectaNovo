from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class ComentarioDTO(BaseModel):
    id_postagem_artigo: int
    texto: str
    data_comentario: Optional[datetime] = None
    data_moderacao: Optional[datetime] = None

    @field_validator('texto')
    @classmethod
    def validate_texto(cls, texto):
        if not texto or not texto.strip():
            raise ValueError('Texto do comentário é obrigatório')
        if len(texto.split()) < 5:
            raise ValueError('Texto do comentário muito curto')
        if len(texto.strip()) > 2000:
            raise ValueError('Texto do comentário muito longo (máx. 2000 caracteres)')
        return texto.strip()

