from pydantic import BaseModel, Field
from typing import Optional


class ComentarioDTO(BaseModel):
    conteudo: str = Field(..., min_length=1, max_length=300)
    id_postagem_feed: Optional[int] = Field(None, gt=0)
    id_postagem_artigo: Optional[int] = Field(None, gt=0)


class EditarComentarioDTO(BaseModel):
    id_comentario: int = Field(..., gt=0)
    conteudo: str = Field(..., min_length=1, max_length=300)


class DenunciaComentarioDTO(BaseModel):
    id_comentario: int = Field(..., gt=0)
    motivo: str = Field(..., min_length=5, max_length=200)