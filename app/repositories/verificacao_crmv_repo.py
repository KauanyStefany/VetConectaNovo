from typing import Optional, List
from app.models.verificacao_crmv_model import VerificacaoCRMV
from app.models.enums import VerificacaoStatus
from app.db.queries import verificacao_crmv_sql
from app.db.connection import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(verificacao_crmv_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de verificação CRMV: {e}")
        return False

def inserir(verificacao: VerificacaoCRMV) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(verificacao_crmv_sql.INSERIR, (
            verificacao.id_veterinario,
            verificacao.id_administrador,
            verificacao.status_verificacao.value
        ))
        return cursor.lastrowid


def atualizar(id_veterinario: int, novo_status: VerificacaoStatus, id_administrador: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(verificacao_crmv_sql.ATUALIZAR, (novo_status.value, id_administrador, id_veterinario))
        return cursor.rowcount > 0


def excluir(id_veterinario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(verificacao_crmv_sql.EXCLUIR, (id_veterinario,))
        return cursor.rowcount > 0


def obter_todos_paginado(limite: int, offset: int) -> List[VerificacaoCRMV]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM verificacao_crmv ORDER BY id_verificacao_crmv LIMIT ? OFFSET ?", (limite, offset))
        rows = cursor.fetchall()
        return [
            VerificacaoCRMV(
                id_verificacao_crmv=row["id_verificacao_crmv"],
                id_veterinario=row["id_veterinario"],
                id_administrador=row["id_administrador"],
                data_verificacao=row["data_verificacao"],
                status_verificacao=VerificacaoStatus(row["status_verificacao"])
            )
            for row in rows]


def obter_por_id(id_verificacao_crmv: int) -> Optional[VerificacaoCRMV]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM verificacao_crmv WHERE id_verificacao_crmv = ?", (id_verificacao_crmv,))
        row = cursor.fetchone()
        if row:
            return VerificacaoCRMV(
                id_verificacao_crmv=row["id_verificacao_crmv"],
                id_veterinario=row["id_veterinario"],
                id_administrador=row["id_administrador"],
                data_verificacao=row["data_verificacao"],
                status_verificacao=VerificacaoStatus(row["status_verificacao"])
            )
        return None
