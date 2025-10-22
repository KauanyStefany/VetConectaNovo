from datetime import datetime
from typing import Optional, List
from model.postagem_artigo_model import PostagemArtigo
from sql.postagem_artigo_sql import *
from util.db_util import get_connection
from routes.veterinario import postagem_artigo_routes

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de postagem_artigo: {e}")
        return False


def inserir(postagem: PostagemArtigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR,
            (
                postagem.id_veterinario,
                postagem.titulo,
                postagem.conteudo,
                postagem.id_categoria_artigo,
            ),
        )
        return cursor.lastrowid


def atualizar(postagem: PostagemArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR,
            (
                postagem.titulo,
                postagem.conteudo,
                postagem.id_categoria_artigo,
                postagem.id_postagem_artigo,
            ),
        )
        return cursor.rowcount > 0


def incrementar_visualizacoes(id_postagem_artigo: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INCREMENTAR_VISUALIZACOES, (id_postagem_artigo,))
        return cursor.rowcount > 0


def excluir(id_postagem_artigo: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_postagem_artigo,))
        return cursor.rowcount > 0


def obter_pagina(pagina: int, tamanho_pagina: int) -> List[PostagemArtigo]:
    limite = tamanho_pagina
    offset = (pagina - 1) * tamanho_pagina
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        return [
            PostagemArtigo(
                id_postagem_artigo=row["id_postagem_artigo"],
                id_veterinario=row["id_veterinario"],
                titulo=row["titulo"],
                conteudo=row["conteudo"],
                id_categoria_artigo=row["id_categoria_artigo"],
                data_publicacao=datetime.strptime(row["data_publicacao"], "%Y-%m-%d %H:%M:%S").date(),
                visualizacoes=row["visualizacoes"],
            )
            for row in rows
        ]


def obter_por_id(id_postagem_artigo: int) -> Optional[PostagemArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_postagem_artigo,))
        row = cursor.fetchone()
        if row:
            return PostagemArtigo(
                id_postagem_artigo=row["id_postagem_artigo"],
                id_veterinario=row["id_veterinario"],
                titulo=row["titulo"],
                conteudo=row["conteudo"],
                id_categoria_artigo=row["id_categoria_artigo"],
                data_publicacao=datetime.strptime(row["data_publicacao"], "%Y-%m-%d %H:%M:%S").date(),
                visualizacoes=row["visualizacoes"],
            )
        return None


def obter_recentes_com_dados(limite: int) -> List[dict]:
    """Retorna os artigos mais recentes com dados do veterinário e categoria."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_RECENTES_COM_DADOS, (limite,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def obter_pagina_com_dados(pagina: int, tamanho_pagina: int) -> List[dict]:
    """Retorna uma página de artigos com dados do veterinário e categoria."""
    limite = tamanho_pagina
    offset = (pagina - 1) * tamanho_pagina
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PAGINA_COM_DADOS, (limite, offset))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def obter_por_categoria_com_dados(id_categoria: int, pagina: int, tamanho_pagina: int) -> List[dict]:
    """Retorna artigos de uma categoria específica com dados do veterinário e categoria."""
    limite = tamanho_pagina
    offset = (pagina - 1) * tamanho_pagina
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CATEGORIA_COM_DADOS, (id_categoria, limite, offset))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def importar(postagem: PostagemArtigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            IMPORTAR,
            (
                postagem.id_postagem_artigo,
                postagem.id_veterinario,
                postagem.titulo,
                postagem.conteudo,
                postagem.id_categoria_artigo,
                postagem.visualizacoes,
            ),
        )
        return postagem.id_postagem_artigo


def contar_total() -> int:
    """Retorna o total de artigos publicados."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_TOTAL)
        row = cursor.fetchone()
        return row["total"] if row else 0


def contar_por_categoria(id_categoria: int) -> int:
    """Retorna o total de artigos de uma categoria específica."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_POR_CATEGORIA, (id_categoria,))
        row = cursor.fetchone()
        return row["total"] if row else 0


def obter_por_veterinario(id_veterinario: int) -> list[PostagemArtigo]:
    """Retorna todos os artigos de um veterinário ordenados por data de publicação"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pa.*, u.nome as nome_veterinario, v.numero_crmv
            FROM postagem_artigo pa
            JOIN veterinario v ON pa.id_veterinario = v.id_veterinario
            JOIN usuario u ON v.id_veterinario = u.id_usuario
            WHERE pa.id_veterinario = ?
            ORDER BY pa.data_publicacao DESC
        """, (id_veterinario,))
        rows = cursor.fetchall()
        return [PostagemArtigo(
            id_postagem_artigo=row["id_postagem_artigo"],
            id_veterinario=row["id_veterinario"],
            titulo=row["titulo"],
            conteudo=row["conteudo"],
            id_categoria_artigo=row["id_categoria_artigo"],
            data_publicacao=datetime.strptime(row["data_publicacao"], "%Y-%m-%d %H:%M:%S").date(),
            visualizacoes=row["visualizacoes"]
        ) for row in rows]