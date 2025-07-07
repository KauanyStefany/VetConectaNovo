from dataclasses import dataclass
from datetime import date
from typing import Optional
from data.tutor_model import Tutor

@dataclass
class PostagemFeed:
    id_postagem_feed: int
    tutor: Optional[Tutor] = None
    imagem: str
    descricao: str
    data_postagem: date
