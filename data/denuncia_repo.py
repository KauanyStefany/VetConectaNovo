from typing import Optional, List
from data.denuncia_model import Denuncia
from data.denuncia_sql import *
from util import get_connection


def criar_tabela_denuncia() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir_denuncia(denuncia: Denuncia) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            denuncia.id_usuario,
            denuncia.id_admin,
            denuncia.motivo,
            denuncia.data_denuncia,  # <- adicionar aqui
            denuncia.status
        ))
        return cursor.lastrowid
    

def atualizar_denuncia(denuncia: Denuncia) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            denuncia.id_usuario,
            denuncia.id_admin,
            denuncia.motivo,
            denuncia.data_denuncia,
            denuncia.status,
            denuncia.id_denuncia
        ))
        return cursor.rowcount > 0


def excluir_denuncia(id_denuncia: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_denuncia,))
        return cursor.rowcount > 0

# def obter_todas_denuncias_paginadas(limite: int, offset: int) -> List[Denuncia]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_TODAS_DENUNCIAS_PAGINADAS, (limite, offset))
#         rows = cursor.fetchall()
#         return [Denuncia(**row) for row in rows]

def obter_todas_denuncias_paginadas(limite: int, offset: int) -> List[Denuncia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS_DENUNCIAS_PAGINADAS, (limite, offset))
        rows = cursor.fetchall()

        denuncias = []
        for row in rows:
            dados = {
                "id_denuncia": row["id_denuncia"],
                "id_usuario": row["id_usuario"],
                "id_admin": row["id_admin"],
                "motivo": row["motivo"],
                "data_denuncia": row["data_denuncia"],
                "status": row["status"]
            }
            denuncias.append(Denuncia(**dados))
        return denuncias


# def obter_denuncia_por_id(id_denuncia: int) -> Optional[Denuncia]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_POR_ID, (id_denuncia,))
#         row = cursor.fetchone()
#         denuncia = Denuncia(
#             id_denuncia=row["id_denuncia"],
#             id_usuario=row["id_usuario"],
#             id_admin=row["id_admin"],
#             motivo = row["motivo"],
#             data_denuncia = row["data_denuncia"],
#             status = row["status"]
#         )
#         return denuncia

def obter_denuncia_por_id(id_denuncia: int) -> Optional[Denuncia]:
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
            status=row["status"]
        )
        return denuncia
    