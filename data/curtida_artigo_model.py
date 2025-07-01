from dataclasses import dataclass
from data.postagem_artigo_model import PostagemArtigo
from data.usuario_model import Usuario

@dataclass
class CurtidaArtigo:
    usuario: Usuario
    artigo: PostagemArtigo
    data_curtida: str