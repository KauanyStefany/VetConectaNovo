CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS categoria_artigo (
    id_categoria_artigo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cor TEXT NOT NULL
);
"""

INSERIR = """
INSERT INTO categoria_artigo (nome, cor)
VALUES (?, ?);
"""

ATUALIZAR = """
UPDATE categoria_artigo
SET nome = ?, cor = ?
WHERE id_categoria_artigo = ?;
"""

EXCLUIR = """
DELETE FROM categoria_artigo
WHERE id_categoria_artigo = ?;
"""

OBTER_PAGINA = """
SELECT
    id_categoria_artigo,
    nome,
    cor
FROM categoria_artigo
ORDER BY nome
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT
    id_categoria_artigo,
    nome,
    cor
FROM categoria_artigo
WHERE id_categoria_artigo = ?;
"""

IMPORTAR = """
INSERT INTO categoria_artigo (id_categoria_artigo, nome, cor)
VALUES (?, ?, ?);
"""