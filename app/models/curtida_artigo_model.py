from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CurtidaArtigo:
    id_usuario: int
    id_postagem_artigo: int
    data_curtida: Optional[datetime] = None
