from typing import Optional, List
from app.models.curtida_feed_model import CurtidaFeed
from app.db.queries import curtida_feed_sql
from app.db.connection import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(curtida_feed_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de curtida_feed: {e}")
        return False


def inserir(curtida: CurtidaFeed) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(curtida_feed_sql.INSERIR, (curtida.id_usuario, curtida.id_postagem_feed))
        return cursor.rowcount > 0


def excluir(id_usuario: int, id_postagem_feed: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(curtida_feed_sql.EXCLUIR, (id_usuario, id_postagem_feed))
        return cursor.rowcount > 0


def OBTER_PAGINA(limite: int, offset: int) -> List[CurtidaFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(curtida_feed_sql.OBTER_PAGINA, (limite, offset))
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
        cursor.execute(curtida_feed_sql.OBTER_POR_ID, (id_usuario, id_postagem_feed))
        row = cursor.fetchone()
        if row:
            return CurtidaFeed(
                id_usuario=id_usuario,
                id_postagem_feed=id_postagem_feed,
                data_curtida=row["data_curtida"],
            )
        return None
