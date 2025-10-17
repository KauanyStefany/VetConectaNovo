from dataclasses import dataclass
from datetime import date


@dataclass
class PostagemArtigo:
    id_postagem_artigo: int
    id_veterinario: int
    titulo: str
    conteudo: str
    id_categoria_artigo: int
    data_publicacao: date
    visualizacoes: int
