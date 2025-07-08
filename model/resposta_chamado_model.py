from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class RespostaChamado:
    id_resposta_chamado: Optional[int] = None     
    id_chamado: int = 0
    titulo: str = ""
    descricao: str = ""
    data: Optional[date] = None  