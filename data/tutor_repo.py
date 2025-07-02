from typing import Any, Optional
from data import usuario_repo
from data.tutor_model import Tutor
import data.tutor_sql as tutor_sql
from data.usuario_model import Usuario
import data.usuario_sql as usuario_sql
from util import get_connection

  
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
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Primeiro inserir o usuário
            cursor.execute(usuario_sql.INSERIR, (tutor.nome, tutor.email, tutor.senha, tutor.telefone))
            id_usuario = cursor.lastrowid
            
            # Depois inserir na tabela tutor
            cursor.execute(tutor_sql.INSERIR, (id_usuario,))
            
            return id_usuario
    except Exception as e:
        print(f"Erro ao inserir tutor: {e}")
        return None

def atualizar_tutor(tutor: Tutor) -> bool:
    return usuario_repo.atualizar_usuario(tutor)
    
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
                    telefone=row["telefone"]
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
                telefone=row["telefone"]
            )
            return tutor
    except Exception as e:
        print(f"Erro ao obter tutor por ID: {e}")
        return None