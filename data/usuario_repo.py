from typing import Any, Optional
from data.usuario_model import Usuario
from data.usuario_sql import *
from util import get_connection


def criar_tabela_usuario() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.telefone))
        return cursor.lastrowid


def atualizar_usuario(usuario: Usuario) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            usuario.nome,
            usuario.email,
            usuario.telefone,
            usuario.id_usuario))
        return cursor.rowcount > 0
    
def atualizar_senha_usuario(id_usuario: int, senha: str) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_SENHA, (senha, id_usuario))
        return (cursor.rowcount > 0)
    
def excluir_usuario(id_usuario: int) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_usuario,))
        return (cursor.rowcount > 0)

def obter_todos_usuarios_paginado(limite: int, offset: int) -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                id_usuario=row["id_usuario"], 
                nome=row["nome"], 
                email=row["email"], 
                senha=row["senha"], 
                telefone=row["telefone"]
            ) 
            for row in rows]
        return usuarios

def obter_usuario_por_id(id_usuario: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_usuario,))
        row = cursor.fetchone()
        usuario = Usuario(
            id_usuario=row["id_usuario"], 
            nome=row["nome"], 
            email=row["email"], 
            senha=row["senha"], 
            telefone=row["telefone"])
        return usuario
