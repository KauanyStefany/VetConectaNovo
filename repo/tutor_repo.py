from typing import Any, Optional
from repo import usuario_repo
from model.tutor_model import Tutor
import sql.tutor_sql as tutor_sql
from model.usuario_model import Usuario
import sql.usuario_sql as usuario_sql
from util.db_util import get_connection

  
def criar_tabela_tutor() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(tutor_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de tutor: {e}")
        return False

def inserir_tutor(tutor: Tutor) -> Optional[int]:
    id_tutor = usuario_repo.inserir_usuario(tutor)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            tutor_sql.INSERIR,
            (id_tutor, tutor.quantidade_pets, tutor.descricao_pets)
        )
        return id_tutor
    
def atualizar_tutor(tutor: Tutor) -> bool:
    # Atualizar dados do usuario tutor
    usuario_atualizado = usuario_repo.atualizar_usuario(tutor)
    if usuario_atualizado:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(tutor_sql.ATUALIZAR, (tutor.quantidade_pets, tutor.descricao_pets, tutor.id_usuario))
            return cursor.rowcount > 0
    return False
    
def excluir_tutor(id_tutor: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Primeiro excluir da tabela tutor
            cursor.execute(tutor_sql.EXCLUIR, (id_tutor,))
            tutor_excluido = cursor.rowcount > 0
            
            # Depois excluir da tabela usuario
            if tutor_excluido:
                cursor.execute(usuario_sql.EXCLUIR, (id_tutor,))
                usuario_excluido = cursor.rowcount > 0
                return usuario_excluido
            
            return False
    except Exception as e:
        print(f"Erro ao excluir tutor: {e}")
        return False

def obter_tutores_por_pagina(limite: int, offset: int) -> list[Tutor]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(tutor_sql.OBTER_TODOS_PAGINADO, (limite, offset))
            rows = cursor.fetchall()
            tutores = []
            for row in rows:
                tutor = Tutor(
                    id_usuario=row["id_tutor"],
                    nome=row["nome"],
                    email=row["email"],
                    senha="",  # Não expor senha
                    telefone=row["telefone"],
                    quantidade_pets=row["quantidade_pets"] if "quantidade_pets" in row.keys() else 0,
                    descricao_pets=row["descricao_pets"] if "descricao_pets" in row.keys() else None
                )
                tutores.append(tutor)
            
            return tutores
    except Exception as e:
        print(f"Erro ao obter tutores paginado: {e}")
        return []

    
def obter_por_id(id_tutor: int) -> Optional[Tutor]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(tutor_sql.OBTER_POR_ID, (id_tutor,))
            row = cursor.fetchone()
            
            if row is None:
                return None
                
            tutor = Tutor(
                id_usuario=row["id_tutor"],
                nome=row["nome"],
                email=row["email"],
                senha="",  # Não expor senha
                telefone=row["telefone"],
                quantidade_pets=row["quantidade_pets"] if "quantidade_pets" in row.keys() else 0,
                descricao_pets=row["descricao_pets"] if "descricao_pets" in row.keys() else None
            )
            return tutor
    except Exception as e:
        print(f"Erro ao obter tutor por ID: {e}")
        return None