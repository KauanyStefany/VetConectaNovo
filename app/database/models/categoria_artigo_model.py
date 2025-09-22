from dataclasses import dataclass
from typing import Optional

@dataclass
class CategoriaArtigo:
    id_categoria_artigo: int
    nome: str
    descricao: Optional[str] = None