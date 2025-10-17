from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CurtidaFeed:
    id_usuario: int
    id_postagem_feed: int
    data_curtida: Optional[datetime] = None
