from dataclasses import dataclass
from datetime import date

@dataclass
class PostagemFeed:
    id_postagem_feed: int
    id_tutor: int
    descricao: str
    data_postagem: date
