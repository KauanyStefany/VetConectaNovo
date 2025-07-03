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
        print(f"Erro ao criar tabela de verificação CRMV: {e}")
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


def atualizar(id_veterinario: int, novo_status: str, id_admin: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (novo_status, id_admin, id_veterinario))
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
                veterinario=Veterinario(
                    id_usuario=row["id_veterinario"], 
                    nome=row["nome_veterinario"],
                    email=row["email_veterinario"],
                    senha="",
                    telefone=row["telefone_veterinario"],
                    crmv=row["crmv"],
                    verificado=row["veterinario_verificado"],
                    bio=row["bio_veterinario"]
                ),
                administrador=Administrador(
                    id_admin=row["id_admin"],
                    nome=row["nome_admin"],
                    email=row["email_admin"],
                    senha=row["senha_admin"]  # <-- ADICIONADO
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
                id_verificacao=row["id"],
                veterinario=Veterinario(
                    id_usuario=row["id_veterinario"],
                    nome=row["nome_veterinario"],
                    email=row["email_veterinario"],
                    senha="",  # se quiser, pode buscar senha do veterinário, mas normalmente não se expõe
                    telefone=row["telefone_veterinario"],
                    crmv=row["crmv"],
                    verificado=row["veterinario_verificado"],
                    bio=row["bio_veterinario"]
                ),
                administrador=Administrador(
                    id_admin=row["id_admin"],
                    nome=row["nome_admin"],
                    email=row["email_admin"],
                    senha=row["senha_admin"]  # <-- ADICIONADO
                ),
                data_verificacao=row["data_verificacao"],
                status=row["status_verificacao"]
            )
    return None
