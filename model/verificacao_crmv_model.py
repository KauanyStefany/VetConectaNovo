from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from model.enums import VerificacaoStatus

@dataclass
class VerificacaoCRMV:
    id_verificacao_crmv: int
    id_veterinario: int
    id_administrador: Optional[int]
    data_verificacao: datetime
    status_verificacao: VerificacaoStatus
