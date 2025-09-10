from typing import Optional, List
from model.comentario_model import Comentario
from sql.comentario_sql import *
from model.postagem_artigo_model import PostagemArtigo
from model.usuario_model import Usuario
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

def inserir(comentario: Comentario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            comentario.id_usuario,
            comentario.id_postagem_artigo,
            comentario.texto
        ))
        return cursor.lastrowid

def atualizar(comentario: Comentario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            comentario.texto,
            comentario.data_moderacao,
            comentario.id_comentario
        ))
        return cursor.rowcount > 0

def excluir(id_comentario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_comentario,))
        return cursor.rowcount > 0

def obter_todos_paginado(limite: int, offset: int) -> List[Comentario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            Comentario(
                id_comentario=row["id_comentario"],
                id_usuario=row["id_usuario"],
                id_postagem_artigo=row["id_postagem_artigo"],
                texto=row["texto"],
                data_comentario=row["data_comentario"],
                data_moderacao=row["data_moderacao"]
            )
            for row in rows]

def obter_por_id(id_comentario: int) -> Optional[Comentario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_comentario,))
        row = cursor.fetchone()
        if row:
            return Comentario(
                id_comentario=row["id_comentario"],
                id_usuario=row["id_usuario"],
                id_postagem_artigo=row["id_postagem_artigo"],
                texto=row["texto"],
                data_comentario=row["data_comentario"],
                data_moderacao=row["data_moderacao"])
        return None