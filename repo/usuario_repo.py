from typing import Any, Optional
from model.usuario_model import Usuario
from sql.usuario_sql import *
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
            usuario.telefone,
            usuario.perfil,
            usuario.foto,
            usuario.token_redefinicao,
            usuario.data_token,
            usuario.data_cadastro))
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
                telefone=row["telefone"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                data_cadastro=row["data_cadastro"]
            ) 
            for row in rows]
        return usuarios

def obter_usuario_por_id(id_usuario: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_usuario,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Usuario(
            id_usuario=row["id_usuario"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            telefone=row["telefone"],
            perfil=row["perfil"],
            foto=row["foto"],
            token_redefinicao=row["token_redefinicao"],
            data_token=row["data_token"],
            data_cadastro=row["data_cadastro"]
        )
    

def obter_por_email(email: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                    id=row["id"], 
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    telefone=row["telefone"],
                    perfil=row["perfil"],
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"],
                    data_cadastro=row["data_cadastro"]
            )
            return usuario
        return None

def atualizar_token(email: str, token: str, data_expiracao: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_TOKEN, (token, data_expiracao, email))
        return (cursor.rowcount > 0)

def atualizar_foto(id: int, caminho_foto: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return (cursor.rowcount > 0)

def obter_por_token(token: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_TOKEN, (token,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                    id=row["id"], 
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    telefone=row["telefone"],
                    perfil=row["perfil"],
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"],
                    data_cadastro=row["data_cadastro"]
            )
            return usuario
        return None

def limpar_token(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET token_redefinicao=NULL, data_token=NULL WHERE id=?", (id,))
        return (cursor.rowcount > 0)

def obter_todos_por_perfil(perfil: str) -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE perfil=? ORDER BY nome", (perfil,))
        rows = cursor.fetchall()
        usuarios = []
        for row in rows:
            usuario = Usuario(
                id=row["id"], 
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                telefone=row["telefone"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                data_cadastro=row["data_cadastro"]
            )
            usuarios.append(usuario)
        return usuarios

