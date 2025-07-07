from dataclasses import dataclass
from datetime import date
from typing import Optional
from data.tutor_model import Tutor

@dataclass
class PostagemFeed:
    id_postagem_feed: int
    id_tutor: int
    imagem: Optional[str]
    descricao: str
    data_postagem: date
    tutor: Optional[Tutor] = None
