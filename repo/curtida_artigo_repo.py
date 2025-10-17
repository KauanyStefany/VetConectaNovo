from typing import Optional, List
from datetime import datetime
from model.curtida_artigo_model import CurtidaArtigo
from sql.curtida_artigo_sql import *
from util.db_util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de curtidas de artigo: {e}")
        return False


def inserir(curtida: CurtidaArtigo) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                INSERIR,
                (curtida.id_usuario, curtida.id_postagem_artigo, curtida.data_curtida),
            )
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao inserir curtida: {e}")
        return False


def excluir(id_usuario: int, id_postagem_artigo: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(EXCLUIR, (id_usuario, id_postagem_artigo))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir curtida: {e}")
        return False


def obter_pagina(limite: int, offset: int) -> List[CurtidaArtigo]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_PAGINA, (limite, offset))
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
            cursor.execute(OBTER_POR_ID, (id_usuario, id_postagem_artigo))
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
