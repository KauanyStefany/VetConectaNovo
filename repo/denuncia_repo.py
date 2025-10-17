from typing import Optional, List
from model.denuncia_model import Denuncia
from model.enums import DenunciaStatus
from sql.denuncia_sql import *
from util.db_util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir(denuncia: Denuncia) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR,
            (
                denuncia.id_usuario,
                denuncia.id_admin,
                denuncia.motivo,
                denuncia.data_denuncia,
                denuncia.status.value,
            ),
        )
        return cursor.lastrowid


def atualizar(denuncia: Denuncia) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR,
            (
                denuncia.id_usuario,
                denuncia.id_admin,
                denuncia.motivo,
                denuncia.data_denuncia,
                denuncia.status.value,
                denuncia.id_denuncia,
            ),
        )
        return cursor.rowcount > 0


def excluir(id_denuncia: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_denuncia,))
        return cursor.rowcount > 0


def obter_pagina(limite: int, offset: int) -> List[Denuncia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PAGINA, (limite, offset))
        rows = cursor.fetchall()

        denuncias = []
        for row in rows:
            dados = {
                "id_denuncia": row["id_denuncia"],
                "id_usuario": row["id_usuario"],
                "id_admin": row["id_admin"],
                "motivo": row["motivo"],
                "data_denuncia": row["data_denuncia"],
                "status": DenunciaStatus(row["status"]),
            }
            denuncias.append(Denuncia(**dados))
        return denuncias


def obter_por_id(id_denuncia: int) -> Optional[Denuncia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_denuncia,))
        row = cursor.fetchone()
        if row is None:
            return None  # <- evita erro
        denuncia = Denuncia(
            id_denuncia=row["id_denuncia"],
            id_usuario=row["id_usuario"],
            id_admin=row["id_admin"],
            motivo=row["motivo"],
            data_denuncia=row["data_denuncia"],
            status=DenunciaStatus(row["status"]),
        )
        return denuncia
