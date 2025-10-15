from datetime import datetime
from typing import Optional, List
from repo import tutor_repo, veterinario_repo
from app.models.seguida_model import Seguida
from app.db.queries import seguida_sql
from app.models.tutor_model import Tutor
from app.db.connection import get_connection
from app.models.veterinario_model import Veterinario


def criar_tabela_seguida() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(seguida_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de seguidas: {e}")
        return False


def inserir_seguida(seguida: Seguida) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(seguida_sql.INSERIR, (
                seguida.id_veterinario,
                seguida.id_tutor
            ))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao inserir seguida: {e}")
        return False


def excluir_seguida(id_veterinario: int, id_tutor: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(seguida_sql.EXCLUIR, (id_veterinario, id_tutor))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir seguida: {e}")
        return False


def obter_seguidas_paginado(pagina: int, tamanho_pagina: int) -> List[Seguida]:
    limite = tamanho_pagina
    offset = (pagina - 1) * tamanho_pagina
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(seguida_sql.OBTER_TODOS_PAGINADO, (limite, offset))
            rows = cursor.fetchall()
            return [
               Seguida(
                    id_veterinario=row["id_veterinario"],
                    id_tutor=row["id_tutor"],
                    data_inicio=datetime.strptime(row["data_inicio"][:10], "%Y-%m-%d").date()
                )
                for row in rows]
    except Exception as e:
        print(f"Erro ao obter seguidas paginado: {e}")
        return []


def obter_seguida_por_id(id_veterinario: int, id_tutor: int) -> Optional[Seguida]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(seguida_sql.OBTER_POR_ID, (id_veterinario, id_tutor))
            row = cursor.fetchone()
            if row:
                return Seguida(
                    id_veterinario=row["id_veterinario"],
                    id_tutor=row["id_tutor"],
                    data_inicio=datetime.strptime(row["data_inicio"][:10], "%Y-%m-%d").date()
                )
            return None
    except Exception as e:
        print(f"Erro ao obter seguida por ID: {e}")
        return None