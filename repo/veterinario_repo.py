from typing import Optional, List
from sql import veterinario_sql, usuario_sql
from model.usuario_model import Usuario
from model.veterinario_model import Veterinario
from sql.veterinario_sql import *
from util.db_util import get_connection


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
    """Insere veterinário e usuário em uma única transação atômica."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Inserir usuário
        cursor.execute(usuario_sql.INSERIR, (
            vet.nome,
            vet.email,
            vet.senha,
            vet.telefone,
            vet.perfil
        ))
        id_veterinario = cursor.lastrowid

        # Inserir veterinário
        cursor.execute(veterinario_sql.INSERIR, (
            id_veterinario,
            vet.crmv,
            vet.bio
        ))

        return id_veterinario


def atualizar_veterinario(vet: Veterinario) -> bool:
    """Atualiza veterinário e usuário em uma única transação atômica."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Atualizar usuário
        cursor.execute(usuario_sql.ATUALIZAR, (
            vet.nome,
            vet.email,
            vet.telefone,
            vet.id_usuario
        ))

        # Atualizar veterinário
        cursor.execute(ATUALIZAR, (
            vet.crmv,
            vet.verificado,
            vet.bio,
            vet.id_usuario
        ))

        return cursor.rowcount > 0
    
def atualizar_verificacao(id_veterinario: int, verificado: bool) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_VERIFICACAO, (verificado, id_veterinario))
        return (cursor.rowcount > 0)

def excluir_veterinario(id: int) -> bool:
    """Exclui veterinário e usuário em uma única transação atômica."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Excluir veterinário (deve vir primeiro devido a foreign key)
        cursor.execute(EXCLUIR, (id,))
        excluiu_veterinario = cursor.rowcount > 0

        # Excluir usuário
        cursor.execute(usuario_sql.EXCLUIR, (id,))
        excluiu_usuario = cursor.rowcount > 0

        return excluiu_veterinario and excluiu_usuario

def obter_por_pagina(limit: int, offset: int) -> list[Veterinario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_VETERINARIO_PAGINADO, (limit, offset))
        rows = cursor.fetchall()
        veterinarios = [
            Veterinario(
                id_usuario=row["id_veterinario"],
                nome=row["nome"],
                email=row["email"],
                senha="",
                telefone=row["telefone"],
                perfil=row["perfil"],
                foto=row.get("foto"),
                token_redefinicao=row.get("token_redefinicao"),
                data_token=row.get("data_token"),
                data_cadastro=row.get("data_cadastro"),
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
            senha="",  # Não expor senha
            telefone=row["telefone"],
            perfil=row["perfil"],
            foto=row["foto"],
            data_cadastro=row["data_cadastro"],
            data_token=row["data_token"],
            token_redefinicao=row["token_redefinicao"],
            crmv=row["crmv"],
            verificado=row["verificado"],
            bio=row["bio"]
        )
        return veterinario
