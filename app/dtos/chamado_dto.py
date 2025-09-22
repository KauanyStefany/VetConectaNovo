from pydantic import BaseModel, Field
from typing import Optional


class ChamadoDTO(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=100)
    descricao: str = Field(..., min_length=10, max_length=1000)
    categoria: str = Field(..., min_length=2, max_length=50)


class RespostaChamadoDTO(BaseModel):
    id_chamado: int = Field(..., gt=0)
    resposta: str = Field(..., min_length=10, max_length=1000)


class EditarChamadoDTO(BaseModel):
    id_chamado: int = Field(..., gt=0)
    titulo: str = Field(..., min_length=5, max_length=100)
    descricao: str = Field(..., min_length=10, max_length=1000)
    categoria: str = Field(..., min_length=2, max_length=50)