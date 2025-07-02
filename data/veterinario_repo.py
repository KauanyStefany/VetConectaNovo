from typing import Optional, List
from data import usuario_repo
from data import veterinario_sql
from data.usuario_model import Usuario
from data.veterinario_model import Veterinario
from data.veterinario_sql import *
from util import get_connection


def criar_tabela_veterinario() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

def inserir_veterinario(vet: Veterinario) -> Optional[int]:
    # Inserir dados do usuário (herdados)
    id_veterinario = usuario_repo.inserir_usuario(vet)
    with get_connection() as conn:
        cursor = conn.cursor()
        # Inserir apenas os atributos exclusivos do veterinário
        cursor.execute(
            veterinario_sql.INSERIR,
            (id_veterinario, vet.crmv, vet.verificado, vet.bio)
        )
        return id_veterinario


def atualizar_veterinario(vet: Veterinario) -> bool:
    usuario_repo.atualizar_usuario(vet)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            vet.crmv,
            vet.verificado,
            vet.bio,
            vet.id_usuario
        ))
        return (cursor.rowcount > 0)

def excluir_veterinario(id_veterinario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_veterinario,))
        # usuario_repo.EXCLUIR(id_usuario, cursor)
        return (cursor.rowcount > 0)
    


def obter_todos(limit: int, offset: int) -> list[Veterinario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_VETERINARIO_PAGINADO, (limit, offset))
        rows = cursor.fetchall()
        veterinarios = [
            Veterinario(
                id_veterinario=row["id_veterinario"], 
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                telefone=row["telefone"],
                crmv=row["crmv"],
                verificado=row["verificado"],
                bio=row["bio"]
            ) for row in rows
        ]
        return veterinarios
    

def obter_por_id(id_veterinario: int) -> Optional[Veterinario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_veterinario,))
        row = cursor.fetchone()
        if row is None:
            return None
        veterinario = Veterinario(
            id_usuario=row["id_veterinario"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            telefone=row["telefone"],
            crmv=row["crmv"],
            verificado=row["verificado"],
            bio=row["bio"]
        )
        return veterinario
