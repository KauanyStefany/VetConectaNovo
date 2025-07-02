from typing import Optional, List
from data.chamado_model import Chamado
from data.chamado_sql import *
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


def inserir_chamado(chamado: Chamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            chamado.id_usuario,
            chamado.id_admin,
            chamado.titulo,
            chamado.descricao,
            chamado.status,
            chamado.data
        ))
        return cursor.lastrowid


def atualizar_status_chamado(id_chamado: int, novo_status: str) -> bool:
    if novo_status not in ['aberto', 'em andamento', 'resolvido']:
        raise ValueError("Status inválido. Use: 'aberto', 'em andamento' ou 'resolvido'.")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (novo_status, id_chamado))
        return cursor.rowcount > 0

from data.chamado_sql import ATUALIZAR_STATUS

def atualizar_status_chamado(id_chamado: int, novo_status: str) -> bool:
    if novo_status not in ['aberto', 'em andamento', 'resolvido']:
        raise ValueError("Status inválido. Use: 'aberto', 'em andamento' ou 'resolvido'.")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_STATUS, (novo_status, id_chamado))
        return cursor.rowcount > 0

def excluir_chamado(id_chamado: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_chamado,))
        return cursor.rowcount > 0


def obter_todos_chamados_paginado(offset: int, limite: int) -> List[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            Chamado(
                id=row["id"],
                id_usuario=row["id_usuario"],
                id_admin=row["id_admin"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                status=row["status"],
                data=row["data"]
            )
            for row in rows
        ]



def obter_chamado_por_id(id_chamado: int) -> Optional[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_chamado,))
        row = cursor.fetchone()
        if row:
            return Chamado(
                id=row["id"],
                id_usuario=row["id_usuario"],
                id_admin=row["id_admin"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                status=row["status"],
                data=row["data"]
            )
        return None



