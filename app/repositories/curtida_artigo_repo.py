from typing import Optional, List
from datetime import datetime
from app.models.curtida_artigo_model import CurtidaArtigo
from app.db.queries import curtida_artigo_sql
from app.db.connection import get_connection


def criar_tabela_curtida_artigo() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(curtida_artigo_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de curtidas de artigo: {e}")
        return False


def inserir_curtida_artigo(curtida: CurtidaArtigo) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                curtida_artigo_sql.INSERIR,
                (curtida.id_usuario, curtida.id_postagem_artigo, curtida.data_curtida),
            )
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao inserir curtida: {e}")
        return False


def excluir_curtida(id_usuario: int, id_postagem_artigo: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(curtida_artigo_sql.EXCLUIR, (id_usuario, id_postagem_artigo))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir curtida: {e}")
        return False


def OBTER_PAGINA(limite: int, offset: int) -> List[CurtidaArtigo]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(curtida_artigo_sql.OBTER_PAGINA, (limite, offset))
            rows = cursor.fetchall()
            curtidas = []
            for row in rows:
                # Converter string para datetime se necessário
                data_curtida = row["data_curtida"]
                if isinstance(data_curtida, str):
                    # Tentar diferentes formatos
                    for fmt in ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                        try:
                            data_curtida = datetime.strptime(data_curtida, fmt)
                            break
                        except ValueError:
                            continue
                curtidas.append(
                    CurtidaArtigo(
                        id_usuario=row["id_usuario"],
                        id_postagem_artigo=row["id_postagem_artigo"],
                        data_curtida=data_curtida if isinstance(data_curtida, datetime) else None,
                    )
                )
            return curtidas
    except Exception as e:
        print(f"Erro ao obter curtidas paginadas: {e}")
        return []


def obter_por_id(id_usuario: int, id_postagem_artigo: int) -> Optional[CurtidaArtigo]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(curtida_artigo_sql.OBTER_POR_ID, (id_usuario, id_postagem_artigo))
            row = cursor.fetchone()
            if row:
                # Converter string para datetime se necessário
                data_curtida = row["data_curtida"]
                if isinstance(data_curtida, str):
                    # Tentar diferentes formatos
                    for fmt in ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                        try:
                            data_curtida = datetime.strptime(data_curtida, fmt)
                            break
                        except ValueError:
                            continue
                return CurtidaArtigo(
                    id_usuario=row["id_usuario"],
                    id_postagem_artigo=row["id_postagem_artigo"],
                    data_curtida=data_curtida if isinstance(data_curtida, datetime) else None,
                )
            return None
    except Exception as e:
        print(f"Erro ao obter curtida por ID: {e}")
        return None
