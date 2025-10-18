from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ComentarioArtigo:
    id_comentario_artigo: int
    id_usuario: int
    id_postagem_artigo: int
    texto: str
    data_comentario: datetime
    data_moderacao: Optional[datetime] = None
