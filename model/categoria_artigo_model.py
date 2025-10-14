from dataclasses import dataclass
from typing import Optional

@dataclass
class CategoriaArtigo:
    id_categoria_artigo: int
    nome: str
    cor: str
    imagem: str