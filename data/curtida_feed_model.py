from dataclasses import dataclass
from typing import Optional

@dataclass
class CurtidaFeed:
    id_usuario: int
    id_postagem_feed: int
    data_curtida: Optional[str] = None
