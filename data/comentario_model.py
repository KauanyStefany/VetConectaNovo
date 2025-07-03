from dataclasses import dataclass, field
import datetime
from typing import Optional
from data.usuario_model import Usuario
from data.postagem_artigo_model import PostagemArtigo

@dataclass
class Comentario:
    id: int
    id_usuario: Usuario
    id_artigo: PostagemArtigo
    texto: str
    data_comentario: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d"))
    data_moderacao: Optional[str] = None
