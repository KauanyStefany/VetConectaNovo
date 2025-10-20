from typing import Optional, List
from model.curtida_feed_model import CurtidaFeed
from sql.curtida_feed_sql import *
from util.db_util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de curtida_feed: {e}")
        return False


def inserir(curtida: CurtidaFeed) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (curtida.id_usuario, curtida.id_postagem_feed))
        return cursor.rowcount > 0


def excluir(id_usuario: int, id_postagem_feed: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_usuario, id_postagem_feed))
        return cursor.rowcount > 0


def obter_pagina(limite: int, offset: int) -> List[CurtidaFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        return [
            CurtidaFeed(
                id_usuario=row["id_usuario"],
                id_postagem_feed=row["id_postagem_feed"],
                data_curtida=row["data_curtida"],
            )
            for row in rows
        ]


def obter_por_id(id_usuario: int, id_postagem_feed: int) -> Optional[CurtidaFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_usuario, id_postagem_feed))
        row = cursor.fetchone()
        if row:
            return CurtidaFeed(
                id_usuario=id_usuario,
                id_postagem_feed=id_postagem_feed,
                data_curtida=row["data_curtida"],
            )
        return None


def contar_curtidas_por_postagem(id_postagem_feed: int) -> int:
    """Retorna o total de curtidas de uma postagem."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_CURTIDAS_POR_POSTAGEM, (id_postagem_feed,))
        row = cursor.fetchone()
        return row["total"] if row else 0
