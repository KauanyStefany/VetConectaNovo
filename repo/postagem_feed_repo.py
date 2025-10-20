from datetime import datetime
from typing import Optional, List
from model.postagem_feed_model import PostagemFeed
from sql.postagem_feed_sql import *
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


def inserir(postagem: PostagemFeed) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (postagem.id_tutor, postagem.descricao))
        return cursor.lastrowid


def atualizar(postagem: PostagemFeed) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (postagem.descricao, postagem.id_postagem_feed))
        return cursor.rowcount > 0


def excluir(id_postagem_feed: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_postagem_feed,))
        return cursor.rowcount > 0


def obter_pagina(pagina: int, tamanho_pagina: int) -> List[PostagemFeed]:
    limite = tamanho_pagina
    offset = (pagina - 1) * tamanho_pagina
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        return [
            PostagemFeed(
                id_postagem_feed=row["id_postagem_feed"],
                id_tutor=row["id_tutor"],
                descricao=row["descricao"],
                data_postagem=datetime.strptime(row["data_postagem"][:10], "%Y-%m-%d").date(),
                visualizacoes=row["visualizacoes"],
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
                id_tutor=row["id_tutor"],
                descricao=row["descricao"],
                data_postagem=datetime.strptime(row["data_postagem"][:10], "%Y-%m-%d").date(),
                visualizacoes=row["visualizacoes"],
            )
        return None


def importar(postagem: PostagemFeed) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            IMPORTAR,
            (
                postagem.id_postagem_feed,
                postagem.id_tutor,
                postagem.descricao,
                postagem.data_postagem,
                postagem.visualizacoes,
            ),
        )
        return postagem.id_postagem_feed


def obter_recentes_com_dados(limite: int) -> List[dict]:
    """Retorna os posts mais recentes com dados do tutor."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_RECENTES_COM_DADOS, (limite,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def obter_pagina_com_dados(pagina: int, tamanho_pagina: int) -> List[dict]:
    """Retorna uma página de posts com dados do tutor."""
    limite = tamanho_pagina
    offset = (pagina - 1) * tamanho_pagina
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PAGINA_COM_DADOS, (limite, offset))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def contar_total() -> int:
    """Retorna o total de posts no feed."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_TOTAL)
        row = cursor.fetchone()
        return row["total"] if row else 0


def obter_por_id_com_dados(id_postagem_feed: int) -> Optional[dict]:
    """Retorna um post por ID com dados completos do tutor."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID_COM_DADOS, (id_postagem_feed,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def incrementar_visualizacoes(id_postagem_feed: int) -> bool:
    """Incrementa o contador de visualizações de um post."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INCREMENTAR_VISUALIZACOES, (id_postagem_feed,))
        return cursor.rowcount > 0
