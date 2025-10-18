from datetime import datetime
from typing import Optional, List
from model.seguida_model import Seguida
from sql.seguida_sql import *
from util.db_util import get_connection


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
            cursor.execute(INSERIR, (seguida.id_seguidor, seguida.id_seguido))
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


def obter_pagina(pagina: int, tamanho_pagina: int) -> List[Seguida]:
    limite = tamanho_pagina
    offset = (pagina - 1) * tamanho_pagina
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_PAGINA, (limite, offset))
            rows = cursor.fetchall()
            return [
                Seguida(
                    id_seguidor=row["id_veterinario"],
                    id_seguido=row["id_tutor"],
                    data_inicio=datetime.strptime(
                        row["data_inicio"][:10], "%Y-%m-%d"
                    ).date(),
                )
                for row in rows
            ]
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
                    id_seguidor=row["id_veterinario"],
                    id_seguido=row["id_tutor"],
                    data_inicio=datetime.strptime(
                        row["data_inicio"][:10], "%Y-%m-%d"
                    ).date(),
                )
            return None
    except Exception as e:
        print(f"Erro ao obter seguida por ID: {e}")
        return None
