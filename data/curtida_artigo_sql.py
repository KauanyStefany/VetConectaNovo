CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS curtida_artigo (
    id_usuario INTEGER NOT NULL,
    id_postagem_artigo INTEGER NOT NULL,
    data_curtida DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id_usuario, id_postagem_artigo),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_postagem_artigo) REFERENCES postagem_artigo(id_artigo)
);  
"""

INSERIR = """
INSERT INTO curtida_artigo (id_usuario, id_postagem_artigo)
VALUES (?, ?);
"""

ATUALIZAR = """
UPDATE curtida_artigo
SET data_curtida = ?
WHERE id_usuario = ? AND id_postagem_artigo = ?;
"""

EXCLUIR = """
DELETE FROM curtida_artigo
WHERE id_usuario = ? 
AND id_postagem_artigo = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT
    ca.id_usuario,
    u.nome AS nome_usuario,
    ca.id_postagem_artigo,
    pa.titulo AS titulo_artigo,
    ca.data_curtida
FROM curtida_artigo ca
INNER JOIN usuario u ON ca.id_usuario = u.id_usuario
INNER JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id_artigo
ORDER BY ca.data_curtida DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT
    ca.id_usuario,
    u.nome AS nome_usuario,
    ca.id_postagem_artigo,
    pa.titulo AS titulo_artigo,
    ca.data_curtida
FROM curtida_artigo ca
INNER JOIN usuario u ON ca.id_usuario = u.id_usuario
INNER JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id_artigo
WHERE ca.id_usuario = ? AND ca.id_postagem_artigo = ?;
"""

# model:

from dataclasses import dataclass
from data.postagem_artigo_model import PostagemArtigo
from data.usuario_model import Usuario

@dataclass
class CurtidaArtigo:
    usuario: Usuario
    artigo: PostagemArtigo
    data_curtida: str

# repo:

from typing import Optional, List
from data.curtida_artigo_model import CurtidaArtigo
from data.curtida_artigo_sql import *
from data.postagem_artigo_model import PostagemArtigo
from data.usuario_model import Usuario
from util import get_connection


def criar_tabela_curtida_artigo() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de curtidas de artigo: {e}")
        return False


def inserir_curtida_artigo(curtida: CurtidaArtigo) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (curtida.usuario.id, curtida.artigo.id))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao inserir curtida: {e}")
        return False


def excluir_curtida(id_usuario: int, id_postagem_artigo: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(EXCLUIR, (id_usuario, id_postagem_artigo))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir curtida: {e}")
        return False


def obter_todos_paginado(limite: int, offset: int) -> List[CurtidaArtigo]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
            rows = cursor.fetchall()
            return [
                CurtidaArtigo(
                    usuario=Usuario(id=row["id_usuario"], nome=row["nome_usuario"]),
                    artigo=PostagemArtigo(id=row["id_postagem_artigo"], titulo=row["titulo_artigo"]),
                    data_curtida=row["data_curtida"]
                )
                for row in rows]
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
                return CurtidaArtigo(
                    usuario=Usuario(id=row["id_usuario"], nome=row["nome_usuario"]),
                    artigo=PostagemArtigo(id=row["id_postagem_artigo"], titulo=row["titulo_artigo"]),
                    data_curtida=row["data_curtida"]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter curtida por ID: {e}")
        return None


