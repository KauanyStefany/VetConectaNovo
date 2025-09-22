from pydantic import BaseModel, Field
from typing import Optional


class PostagemFeedDTO(BaseModel):
    conteudo: str = Field(..., min_length=1, max_length=500)
    foto: Optional[str] = None


class EditarPostagemFeedDTO(BaseModel):
    id_postagem: int = Field(..., gt=0)
    conteudo: str = Field(..., min_length=1, max_length=500)
    foto: Optional[str] = None


class CurtidaFeedDTO(BaseModel):
    id_postagem: int = Field(..., gt=0)
    id_usuario: int = Field(..., gt=0)