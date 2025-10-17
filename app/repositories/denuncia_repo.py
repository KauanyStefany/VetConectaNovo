from typing import Optional, List
from app.models.denuncia_model import Denuncia
from app.models.enums import DenunciaStatus
from app.db.queries import denuncia_sql
from app.db.connection import get_connection


def criar_tabela_denuncia() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(denuncia_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir_denuncia(denuncia: Denuncia) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            denuncia_sql.INSERIR,
            (denuncia.id_usuario, denuncia.id_admin, denuncia.motivo, denuncia.data_denuncia, denuncia.status.value),
        )
        return cursor.lastrowid


def atualizar_denuncia(denuncia: Denuncia) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            denuncia_sql.ATUALIZAR,
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


def excluir_denuncia(id_denuncia: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(denuncia_sql.EXCLUIR, (id_denuncia,))
        return cursor.rowcount > 0


def obter_todas_denuncias_paginadas(limite: int, offset: int) -> List[Denuncia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(denuncia_sql.OBTER_TODAS_DENUNCIAS_PAGINADAS, (limite, offset))
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


def obter_denuncia_por_id(id_denuncia: int) -> Optional[Denuncia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(denuncia_sql.OBTER_POR_ID, (id_denuncia,))
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
