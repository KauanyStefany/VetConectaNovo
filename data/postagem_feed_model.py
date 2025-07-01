from dataclasses import dataclass
from typing import Optional
from data.tutor_model import Tutor

@dataclass
class PostagemFeed:
    id_postagem_feed: int
    tutor: Tutor
    imagem: Optional[str]
    descricao: str
    data_postagem: str
