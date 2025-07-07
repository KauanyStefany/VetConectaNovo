from dataclasses import dataclass
from datetime import date
from typing import Optional
from data.categoria_artigo_model import CategoriaArtigo
from data.veterinario_model import Veterinario

@dataclass
class PostagemArtigo:
    id: int
    id_veterinario: int
    titulo: str
    conteudo: str
    id_categoria_artigo: int
    data_publicacao: date
    visualizacoes: int
    veterinario: Optional[Veterinario] = None
    categoria_artigo: Optional[CategoriaArtigo] = None