from dataclasses import dataclass, field
import datetime
from typing import Optional

from data.postagem_artigo_model import PostagemArtigo
from data.usuario_model import Usuario

@dataclass
class Comentario:
    id: int
    id_usuario: int
    id_artigo: int
    texto: str
    data_comentario: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d"))
    data_moderacao: Optional[str] = None
