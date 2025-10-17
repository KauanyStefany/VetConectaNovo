from typing import Optional, List
from app.models.categoria_artigo_model import CategoriaArtigo
from app.db.queries import categoria_artigo_sql
from app.repositories.base_repository import BaseRepository


class CategoriaArtigoRepository(BaseRepository[CategoriaArtigo]):
    """Repositório para gerenciar categorias de artigos"""

    def _row_to_model(self, row) -> CategoriaArtigo:
        """Converte row do banco para CategoriaArtigo"""
        return CategoriaArtigo(**row)

    def criar_tabela(self) -> bool:
        """Cria a tabela de categorias no banco"""
        try:
            self._executar_query(categoria_artigo_sql.CRIAR_TABELA)
            return True
        except Exception as e:
            print(f"Erro ao criar tabela de categorias: {e}")
            return False

    def inserir(self, categoria: CategoriaArtigo) -> Optional[int]:
        """Insere uma nova categoria"""
        cursor = self._executar_query(
            categoria_artigo_sql.INSERIR,
            (categoria.nome, categoria.cor, categoria.imagem),
        )
        return cursor.lastrowid

    def atualizar(self, categoria: CategoriaArtigo) -> bool:
        """Atualiza uma categoria existente"""
        cursor = self._executar_query(
            categoria_artigo_sql.ATUALIZAR,
            (
                categoria.nome,
                categoria.id_categoria_artigo,
                categoria.cor,
                categoria.imagem,
            ),
        )
        return cursor.rowcount > 0

    def excluir(self, id_categoria: int) -> bool:
        """Exclui uma categoria"""
        cursor = self._executar_query(categoria_artigo_sql.EXCLUIR, (id_categoria,))
        return cursor.rowcount > 0

    def obter_paginado(self, offset: int, limite: int) -> List[CategoriaArtigo]:
        """Obtém categorias paginadas"""
        return self._obter_todos(categoria_artigo_sql.OBTER_PAGINA, (limite, offset))

    def obter_por_id(self, id_categoria: int) -> Optional[CategoriaArtigo]:
        """Obtém uma categoria por ID"""
        return self._obter_um(categoria_artigo_sql.OBTER_POR_ID, (id_categoria,))


# Instância global para manter compatibilidade com código existente
_repo = CategoriaArtigoRepository()


# Funções wrapper para manter compatibilidade
def criar_tabela_categoria_artigo() -> bool:
    return _repo.criar_tabela()


def inserir_categoria(categoria: CategoriaArtigo) -> Optional[int]:
    return _repo.inserir(categoria)


def atualizar_categoria(categoria: CategoriaArtigo) -> bool:
    return _repo.atualizar(categoria)


def excluir_categoria(id_categoria: int) -> bool:
    return _repo.excluir(id_categoria)


def obter_categorias_paginado(offset: int, limite: int) -> List[CategoriaArtigo]:
    return _repo.obter_paginado(offset, limite)


def obter_categoria_por_id(id_categoria: int) -> Optional[CategoriaArtigo]:
    return _repo.obter_por_id(id_categoria)
