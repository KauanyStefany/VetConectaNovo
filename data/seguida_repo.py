from datetime import datetime
from typing import Optional, List
from data import tutor_repo, veterinario_repo
from data.seguida_model import Seguida
from data.seguida_sql import *
from data.tutor_model import Tutor
from util import get_connection
from data.veterinario_model import Veterinario


def criar_tabela_seguida() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de seguidas: {e}")
        return False


def inserir_seguida(seguida: Seguida) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
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
            cursor.execute(EXCLUIR, (id_veterinario, id_tutor))
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
            cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
            rows = cursor.fetchall()
            return [
               Seguida(
                    id_veterinario=row["id_veterinario"],
                    id_tutor=row["id_tutor"],
                    data_inicio=datetime.strptime(row["data_inicio"], "%Y-%m-%d"),
                    veterinario=veterinario_repo.obter_por_id(row["id_veterinario"]),
                    tutor=tutor_repo.obter_por_id(row["id_tutor"]),
                )
                for row in rows]
    except Exception as e:
        print(f"Erro ao obter seguidas paginado: {e}")
        return []


def obter_seguida_por_id(id_veterinario: int, id_tutor: int) -> Optional[Seguida]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (id_veterinario, id_tutor))
            row = cursor.fetchone()
            if row:
                return Seguida(
                    id_veterinario=row["id_veterinario"],
                    id_tutor=row["id_tutor"],
                    data_inicio=datetime.strptime(row["data_inicio"], "%Y-%m-%d"),
                    veterinario=veterinario_repo.obter_por_id(row["id_veterinario"]),
                    tutor=tutor_repo.obter_por_id(row["id_tutor"]),
                )
            return None
    except Exception as e:
        print(f"Erro ao obter seguida por ID: {e}")
        return None