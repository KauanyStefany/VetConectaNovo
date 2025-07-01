from typing import Optional, List
from data.categoria_artigo_model import CategoriaArtigo
from data.categoria_artigo_sql import *
from util import get_connection


def criar_tabela_categoria_artigo() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir_categoria(categoria: CategoriaArtigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (categoria.nome, categoria.descricao))
        return cursor.lastrowid


def atualizar_categoria(categoria: CategoriaArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (categoria.nome, categoria.descricao, categoria.id))
        return cursor.rowcount > 0


def excluir_categoria(id_categoria: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_categoria,))
        return cursor.rowcount > 0


def obter_categorias_paginado(offset: int, limite: int) -> List[CategoriaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [CategoriaArtigo(**row) for row in rows]
    

def obter_categoria_por_id(id_categoria: int) -> Optional[CategoriaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_categoria,))
        row = cursor.fetchone()
        return CategoriaArtigo(**row) if row else None
