from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ArtigoDTO(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=200)
    conteudo: str = Field(..., min_length=10)
    id_categoria: int = Field(..., gt=0)
    foto: Optional[str] = None


class CategoriaArtigoDTO(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: str = Field(..., min_length=5, max_length=500)


class EditarArtigoDTO(BaseModel):
    id_artigo: int = Field(..., gt=0)
    titulo: str = Field(..., min_length=5, max_length=200)
    conteudo: str = Field(..., min_length=10)
    id_categoria: int = Field(..., gt=0)
    foto: Optional[str] = None


class CurtidaArtigoDTO(BaseModel):
    id_artigo: int = Field(..., gt=0)
    id_usuario: int = Field(..., gt=0)