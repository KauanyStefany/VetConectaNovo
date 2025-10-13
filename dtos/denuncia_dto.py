from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

from model.enums import DenunciaStatus


class DenunciaDTO(BaseModel):
    motivo: str
    status: Optional[str] = None
    data_denuncia: Optional[datetime] = None

    @field_validator('motivo')
    @classmethod
    def validate_motivo(cls, motivo):
        if not motivo or not motivo.strip():
            raise ValueError('Motivo é obrigatório')
        if len(motivo.split()) < 5:
            raise ValueError('Motivo deve ter pelo menos 5 palavras')
        return motivo.strip()

    @field_validator('status')
    @classmethod
    def validate_status(cls, status):
        if status is None:
            return DenunciaStatus.PENDENTE.value
        if isinstance(status, DenunciaStatus):
            return status.value
        if status not in {s.value for s in DenunciaStatus}:
            raise ValueError(f'Status inválido. Valores possíveis: {[s.value for s in DenunciaStatus]}')
        return status
