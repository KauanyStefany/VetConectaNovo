from typing import Optional, List
from app.models.resposta_chamado_model import RespostaChamado
from app.db.queries import resposta_chamado_sql
from app.db.connection import get_connection


def criar_tabelas() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(resposta_chamado_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir_resposta(resposta: RespostaChamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            resposta_chamado_sql.INSERIR,
            (resposta.id_chamado, resposta.titulo, resposta.descricao, resposta.data),
        )
        return cursor.lastrowid


def atualizar_resposta(resposta: RespostaChamado) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                resposta_chamado_sql.ATUALIZAR,
                (
                    resposta.id_chamado,
                    resposta.titulo,
                    resposta.descricao,
                    resposta.data,
                    resposta.id_resposta_chamado,
                ),
            )
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar resposta: {e}")
        return False


def excluir_resposta(id_resposta: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(resposta_chamado_sql.EXCLUIR, (id_resposta,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir resposta: {e}")
        return False


def obter_todas_respostas_paginado(limite: int, offset: int) -> List[RespostaChamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(resposta_chamado_sql.OBTER_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        return [
            RespostaChamado(
                id_resposta_chamado=row["id_resposta_chamado"],
                id_chamado=row["id_chamado"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data=row["data"],
            )
            for row in rows
        ]


def obter_resposta_por_id(id_resposta: int) -> Optional[RespostaChamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(resposta_chamado_sql.OBTER_POR_ID, (id_resposta,))
        row = cursor.fetchone()
        if row:
            return RespostaChamado(
                id_resposta_chamado=row["id_resposta_chamado"],
                id_chamado=row["id_chamado"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data=row["data"],
            )
        return None
