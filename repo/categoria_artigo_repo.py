from typing import Optional, List
from model.categoria_artigo_model import CategoriaArtigo
from sql.categoria_artigo_sql import *
from util.db_util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir(categoria: CategoriaArtigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (categoria.nome, categoria.cor, categoria.imagem))
        return cursor.lastrowid


def atualizar(categoria: CategoriaArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR,
            (
                categoria.nome,
                categoria.cor,
                categoria.imagem,
                categoria.id_categoria_artigo,
            ),
        )
        return cursor.rowcount > 0


def excluir(id_categoria: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_categoria,))
        return cursor.rowcount > 0


def obter_pagina(offset: int, limite: int) -> List[CategoriaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        return [CategoriaArtigo(**row) for row in rows]


def obter_por_id(id_categoria: int) -> Optional[CategoriaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_categoria,))
        row = cursor.fetchone()
        return CategoriaArtigo(**row) if row else None
