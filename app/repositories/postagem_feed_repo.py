from datetime import datetime
from typing import Optional, List
from app.models.postagem_feed_model import PostagemFeed
from app.db.queries import postagem_feed_sql
from app.models.tutor_model import Tutor
from app.db.connection import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(postagem_feed_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

def inserir(postagem: PostagemFeed) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_feed_sql.INSERIR, (
            postagem.id_tutor,
            postagem.imagem,
            postagem.descricao
        ))
        return cursor.lastrowid
    
def atualizar(postagem: PostagemFeed) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_feed_sql.ATUALIZAR, (
            postagem.descricao,
            postagem.id_postagem_feed
        ))
        return cursor.rowcount > 0


def excluir(id_postagem_feed: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_feed_sql.EXCLUIR, (id_postagem_feed,))
        return cursor.rowcount > 0

def obter_todos_paginado(pagina: int, tamanho_pagina: int) -> List[PostagemFeed]:
    limite = tamanho_pagina
    offset = (pagina - 1) * tamanho_pagina
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_feed_sql.OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            PostagemFeed(
                id_postagem_feed=row["id_postagem_feed"],
                id_tutor=row["id_tutor"],
                imagem=row["imagem"],
                descricao=row["descricao"],
                data_postagem=datetime.strptime(row["data_postagem"][:10], "%Y-%m-%d").date()
            )
            for row in rows
        ]

def obter_por_id(id_postagem_feed: int) -> Optional[PostagemFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_feed_sql.OBTER_POR_ID, (id_postagem_feed,))
        row = cursor.fetchone()
        if row:
            return PostagemFeed(
                id_postagem_feed=row["id_postagem_feed"],
                id_tutor=row["id_tutor"],
                imagem=row["imagem"],
                descricao=row["descricao"],
                data_postagem=datetime.strptime(row["data_postagem"][:10], "%Y-%m-%d").date()
            )
        return None