from datetime import datetime
from typing import Optional, List
from app.models.postagem_artigo_model import PostagemArtigo
from app.db.queries import postagem_artigo_sql
from app.db.connection import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(postagem_artigo_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de postagem_artigo: {e}")
        return False


def inserir(postagem: PostagemArtigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_artigo_sql.INSERIR, (
            postagem.id_veterinario,
            postagem.titulo,
            postagem.conteudo,
            postagem.id_categoria_artigo
        ))
        return cursor.lastrowid


def atualizar(postagem: PostagemArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_artigo_sql.ATUALIZAR, (
            postagem.titulo,
            postagem.conteudo,
            postagem.id_categoria_artigo,
            postagem.id_postagem_artigo
        ))
        return cursor.rowcount > 0
    
def incrementar_visualizacoes(id_postagem_artigo: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_artigo_sql.INCREMENTAR_VISUALIZACOES, (id_postagem_artigo,))
        return cursor.rowcount > 0


def excluir(id_postagem_artigo: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_artigo_sql.EXCLUIR, (id_postagem_artigo,))
        return cursor.rowcount > 0


def obter_todos_paginado(pagina: int, tamanho_pagina: int) -> List[PostagemArtigo]:
    limite = tamanho_pagina
    offset = (pagina - 1) * tamanho_pagina
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_artigo_sql.OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            PostagemArtigo(
                id_postagem_artigo=row["id_postagem_artigo"],
                id_veterinario=row["id_veterinario"],
                titulo=row["titulo"],
                conteudo=row["conteudo"],
                id_categoria_artigo=row["id_categoria_artigo"],                
                data_publicacao=datetime.strptime(row["data_publicacao"], "%Y-%m-%d %H:%M:%S").date(),
                visualizacoes=row["visualizacoes"])
            for row in rows
        ]


def obter_por_id(id_postagem_artigo: int) -> Optional[PostagemArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(postagem_artigo_sql.OBTER_POR_ID, (id_postagem_artigo,))
        row = cursor.fetchone()
        if row:
            return PostagemArtigo(
                id_postagem_artigo=row["id_postagem_artigo"],
                id_veterinario=row["id_veterinario"],
                titulo=row["titulo"],
                conteudo=row["conteudo"],
                id_categoria_artigo=row["id_categoria_artigo"],                
                data_publicacao=datetime.strptime(row["data_publicacao"], "%Y-%m-%d %H:%M:%S").date(),
                visualizacoes=row["visualizacoes"]
            )
        return None