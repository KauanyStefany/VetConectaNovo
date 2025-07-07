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
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir(postagem: PostagemFeed) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            postagem.id_postagem_feed,
            postagem.tutor.id_usuario,
            postagem.imagem,
            postagem.descricao,
            postagem.data_postagem
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
                tutor=Tutor(id=row["id_tutor"], nome=row["nome_tutor"]),
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
                tutor=Tutor(id=row["id_tutor"], nome=row["nome_tutor"]),
                imagem=row["imagem"],
                descricao=row["descricao"],
                data_postagem=row["data_postagem"]
            )
        return None