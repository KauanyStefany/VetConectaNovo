from dataclasses import dataclass

@dataclass
class CategoriaArtigo:
    id: int
    nome: str
    descricao: str | None  # campo opcional
