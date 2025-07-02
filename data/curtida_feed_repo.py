from typing import Optional, List
from data.postagem_feed_model import PostagemFeed
from data.postagem_feed_sql import *
from data.tutor_model import Tutor
from util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de postagem_feed: {e}")
        return False


def inserir(postagem: PostagemFeed) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            postagem.tutor.id_usuario,  # CORRIGIDO: acessar o ID do tutor através do objeto
            postagem.imagem,
            postagem.descricao
        ))
        return cursor.lastrowid


def atualizar(postagem: PostagemFeed) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            postagem.descricao,
            postagem.id_postagem_feed
        ))
        return cursor.rowcount > 0


def excluir(id_postagem_feed: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_postagem_feed,))
        return cursor.rowcount > 0

def obter_todos_paginado(limite: int, offset: int) -> List[PostagemFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            PostagemFeed(
                id_postagem_feed=row["id_postagem_feed"],
                tutor=Tutor(id_usuario=row["id_tutor"], nome=row["nome_tutor"]),  # CORRIGIDO: usar id_usuario em vez de id
                imagem=row["imagem"],
                descricao=row["descricao"],
                data_postagem=row["data_postagem"]
            )
            for row in rows
        ]


def obter_por_id(id_postagem_feed: int) -> Optional[PostagemFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_postagem_feed,))
        row = cursor.fetchone()
        if row:
            return PostagemFeed(
                id_postagem_feed=row["id_postagem_feed"],
                tutor=Tutor(id_usuario=row["id_tutor"], nome=row["nome_tutor"]),  # CORRIGIDO: usar id_usuario em vez de id
                imagem=row["imagem"],
                descricao=row["descricao"],
                data_postagem=row["data_postagem"]
            )
        return None




















# from typing import Optional, List
# from data.curtida_feed_model import CurtidaFeed
# from data.curtida_feed_sql import *
# from util import get_connection


# def criar_tabela() -> bool:
#     try:
#         with get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(CRIAR_TABELA)
#             return True
#     except Exception as e:
#         print(f"Erro ao criar tabela de categorias: {e}")
#         return False


# def inserir(curtida: CurtidaFeed) -> bool:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(INSERIR, (
#             curtida.id_usuario,
#             curtida.id_postagem_feed
#         ))
#         return cursor.rowcount > 0


# def excluir(id_usuario: int, id_postagem_feed: int) -> bool:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(EXCLUIR, (id_usuario, id_postagem_feed))
#         return cursor.rowcount > 0


# def obter_todos_paginado(limite: int, offset: int) -> List[CurtidaFeed]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
#         rows = cursor.fetchall()
#         return [
#             CurtidaFeed(
#                 id_usuario=row["id_usuario"],
#                 id_postagem_feed=row["id_postagem_feed"],
#                 data_curtida=row["data_curtida"]
#             )
#             for row in rows]


# def obter_por_id(id_usuario: int, id_postagem_feed: int) -> Optional[CurtidaFeed]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_POR_ID, (id_usuario, id_postagem_feed))
#         row = cursor.fetchone()
#         if row:
#             return CurtidaFeed(
#                 id_usuario=id_usuario,
#                 id_postagem_feed=id_postagem_feed,
#                 data_curtida=row["data_curtida"]
#             )
#         return None
