from typing import Optional, List
from data.verificacao_crmv_model import VerificacaoCRMV
from data.verificacao_crmv_sql import *
from util import get_connection
from data.veterinario_model import Veterinario
from data.administrador_model import Administrador


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

def inserir(verificacao: VerificacaoCRMV) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            verificacao.veterinario.id_usuario,
            verificacao.administrador.id_admin,
            verificacao.status_verificacao
        ))
        return cursor.lastrowid


def atualizar(id_veterinario: int, novo_status: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (novo_status, id_veterinario))
        return cursor.rowcount > 0


def excluir(id_veterinario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_veterinario,))
        return cursor.rowcount > 0


def obter_todos_paginado(limite: int, offset: int) -> List[VerificacaoCRMV]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            VerificacaoCRMV(
                id=row["id"],
                veterinario=Veterinario(id_veterinario=row["id_veterinario"], nome=row["nome_veterinario"]),
                administrador=Administrador(
                    id_admin=row["id_admin"],
                    nome=row["nome_admin"],
                    email=row["email_admin"]
                ),
                data_verificacao=row["data_verificacao"],
                status_verificacao=row["status_verificacao"]
            )
            for row in rows]



def obter_por_id(id: int) -> Optional[VerificacaoCRMV]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return VerificacaoCRMV(
                id=row["id"],
                veterinario=Veterinario(id_veterinario=row["id_veterinario"]),
                administrador=Administrador(id_admin=row["id_admin"],nome=row["nome_admin"],email=row["email_admin"]),
                data_verificacao=row["data_verificacao"],
                status_verificacao=row["status_verificacao"])
        return None
