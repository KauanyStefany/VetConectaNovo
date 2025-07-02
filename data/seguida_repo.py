from typing import Optional, List
from data.seguida_model import Seguida
from data.seguida_sql import *
from data.tutor_model import Tutor
from util import get_connection
from data.veterinario_model import Veterinario


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de seguidas: {e}")
        return False


def inserir(seguida: Seguida) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                seguida.id_veterinario.id_usuario,
                seguida.id_tutor.id_usuario))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao inserir seguida: {e}")
        return False


def excluir(id_veterinario: int, id_tutor: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(EXCLUIR, (id_veterinario, id_tutor))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir seguida: {e}")
        return False


def obter_todos_paginado(limite: int, offset: int) -> List[Seguida]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
            rows = cursor.fetchall()
            return [
                Seguida(
                    id_veterinario=Veterinario(id_usuario=row["id_veterinario"], nome=row["nome_veterinario"]),
                    id_tutor=Tutor(id_usuario=row["id_tutor"], nome=row["nome_tutor"]),
                    data_inicio=row["data_inicio"]
                )
                for row in rows]
    except Exception as e:
        print(f"Erro ao obter seguidas paginado: {e}")
        return []


def obter_por_id(id_veterinario: int, id_tutor: int) -> Optional[Seguida]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (id_veterinario, id_tutor))
            row = cursor.fetchone()
            if row:
                return Seguida(
                    id_veterinario=Veterinario(id_usuario=row["id_veterinario"], nome=row["nome_veterinario"]),
                    id_tutor=Tutor(id_usuario=row["id_tutor"], nome=row["nome_tutor"]),
                    data_inicio=row["data_inicio"]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter seguida por ID: {e}")
        return None