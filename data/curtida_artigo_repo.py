from typing import Optional, List
from data.curtida_artigo_model import CurtidaArtigo
from data.curtida_artigo_sql import *
from data.postagem_artigo_model import PostagemArtigo
from data.usuario_model import Usuario
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


def inserir(curtida: CurtidaArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (curtida.id_usuario, curtida.id_artigo))
        return cursor.rowcount > 0

def excluir_curtida(id_usuario: int, id_postagem_artigo: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_usuario, id_postagem_artigo))
        return cursor.rowcount > 0


def obter_todos_paginado(limite: int, offset: int) -> List[CurtidaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            CurtidaArtigo(
                usuario=Usuario(id=row["id_usuario"], nome=row["nome_usuario"]),
                artigo=PostagemArtigo(id=row["id_postagem_artigo"], titulo=row["titulo_artigo"]),
                data_curtida=row["data_curtida"]
            )
            for row in rows]


def obter_por_id(id_usuario: int, id_postagem_artigo: int) -> Optional[CurtidaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_usuario, id_postagem_artigo))
        row = cursor.fetchone()
        if row:
            return CurtidaArtigo(
                usuario=Usuario(id=row["id_usuario"],nome=row["nome_usuario"]),
                artigo=PostagemArtigo(id=row["id_artigo"], nome=row["titulo_artigo"]), #verificar o nome do campo titulo na tabela postagem art.
                data_curtida=row["data_curtida"]
            )
        return None