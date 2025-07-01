from typing import Optional, List
from data.resposta_chamado_model import RespostaChamado
from data.resposta_chamado_sql import *
from util import get_connection

def criar_tabelas() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False
    
def inserir_resposta(resposta: RespostaChamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            resposta.id_chamado,
            resposta.titulo,
            resposta.descricao,
            resposta.data
        ))
        return cursor.lastrowid
    
def obter_todas_respostas_paginado(limite: int, offset: int) -> List[RespostaChamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            RespostaChamado(
                id=row["id"],
                id_chamado=row["id_chamado"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data=row["data"]
            )
            for row in rows
        ]


def obter_resposta_por_id(id_resposta: int) -> Optional[RespostaChamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_resposta,))
        row = cursor.fetchone()
        if row:
            return RespostaChamado(
                id=row["id"],
                id_chamado=row["id_chamado"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data=row["data"]
            )
        return None