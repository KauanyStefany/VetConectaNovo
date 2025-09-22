from pydantic import BaseModel, Field
from typing import Optional


class CategoriaAdminDTO(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: str = Field(..., min_length=5, max_length=500)


class EditarCategoriaAdminDTO(BaseModel):
    id_categoria: int = Field(..., gt=0)
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: str = Field(..., min_length=5, max_length=500)


class VerificacaoUsuarioDTO(BaseModel):
    id_usuario: int = Field(..., gt=0)
    aprovado: bool
    observacoes: Optional[str] = Field(None, max_length=500)


class DenunciaAdminDTO(BaseModel):
    id_denuncia: int = Field(..., gt=0)
    status: str = Field(..., regex="^(pendente|analisada|rejeitada)$")
    observacoes: Optional[str] = Field(None, max_length=500)