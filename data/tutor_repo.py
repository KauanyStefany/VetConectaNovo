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
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

    
def inserir_tutor(tutor: Tutor) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(tutor_sql.INSERIR, (tutor.id_usuario, tutor.nome, tutor.email, tutor.senha))
        return cursor.lastrowid
    



def atualizar_tutor(tutor: Tutor) -> bool:
    return usuario_repo.atualizar_usuario(tutor)
    
def excluir_tutor(id_tutor: int) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(tutor_sql.EXCLUIR, (id_tutor,))
        return (cursor.rowcount > 0)

def obter_todos_tutores_paginado(limite: int, offset: int) -> list[Tutor]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(tutor_sql.OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        tutores = [
            Tutor(
                id_tutor=row["id_tutor"],
                nome=row["nome"],
                email=row["email"],
                telefone=row["telefone"]
            )
            for row in rows]
        return tutores

    
def obter_tutor_por_id(id_tutor: int) -> Optional[Tutor]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(tutor_sql.OBTER_POR_ID, (id_tutor,))
        row = cursor.fetchone()
        tutor = Tutor(
                id_tutor=row["id_tutor"], 
                telefone=row["telefone"])
        return tutor