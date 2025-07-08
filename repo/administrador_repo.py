from typing import Optional, List
from model.administrador_model import Administrador
from sql.administrador_sql import *
from util import get_connection


def criar_tabela_administrador() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de administrador: {e}")
        return False

def inserir_administrador(admin: Administrador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (admin.nome, admin.email, admin.senha))
        return cursor.lastrowid

def atualizar_administrador(admin: Administrador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (admin.nome, admin.email, admin.senha, admin.id_admin))
        return cursor.rowcount > 0
    
def atualizar_senha(id_admin: int, nova_senha: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_SENHA, (nova_senha, id_admin))
        return cursor.rowcount > 0

def excluir_administrador(id_admin: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_admin,))
        return cursor.rowcount > 0

def obter_administradores_paginado(offset: int, limite: int) -> List[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ADMINISTRADORES_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [Administrador(**row) for row in rows]

def obter_administrador_por_id(id_admin: int) -> Optional[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_admin,))
        row = cursor.fetchone()
        return Administrador(**row) if row else None