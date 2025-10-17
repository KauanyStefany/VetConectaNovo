from dataclasses import dataclass


@dataclass
class CategoriaArtigo:
    id_categoria_artigo: int
    nome: str
    cor: str
    imagem: str
