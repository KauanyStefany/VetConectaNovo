from dataclasses import dataclass
from data.categoria_artigo_model import CategoriaArtigo
from data.veterinario_model import Veterinario

@dataclass
class PostagemArtigo:
    id: int
    veterinario: Veterinario
    titulo: str
    conteudo: str
    categoria_artigo: CategoriaArtigo
    data_publicacao: str
    visualizacoes: int