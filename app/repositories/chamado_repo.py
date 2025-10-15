from typing import Optional, List
from app.models.chamado_model import Chamado
from app.models.enums import ChamadoStatus
from app.db.queries import chamado_sql
from app.db.connection import get_connection


def criar_tabela_chamado() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(chamado_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

def inserir_chamado(chamado: Chamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(chamado_sql.INSERIR, (
            chamado.id_usuario,
            chamado.id_admin,
            chamado.titulo,
            chamado.descricao,
            chamado.status.value if hasattr(chamado.status, 'value') else chamado.status,
            chamado.data
        ))
        return cursor.lastrowid

def atualizar_status_chamado(id_chamado: int, novo_status: ChamadoStatus) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(chamado_sql.ATUALIZAR_STATUS, (novo_status.value, id_chamado))
        return cursor.rowcount > 0

def excluir_chamado(id_chamado: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(chamado_sql.EXCLUIR, (id_chamado,))
        return cursor.rowcount > 0

def obter_todos_chamados_paginado(offset: int, limite: int) -> List[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(chamado_sql.OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            Chamado(
                id_chamado=row["id_chamado"],
                id_usuario=row["id_usuario"],
                id_admin=row["id_admin"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                status=ChamadoStatus(row["status"]),
                data=row["data"]
            )
            for row in rows
        ]

def obter_chamado_por_id(id_chamado: int) -> Optional[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(chamado_sql.OBTER_POR_ID, (id_chamado,))
        row = cursor.fetchone()
        if row:
            return Chamado(
                id_chamado=row["id_chamado"],
                id_usuario=row["id_usuario"],
                id_admin=row["id_admin"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                status=ChamadoStatus(row["status"]),
                data=row["data"]
            )
        return None



