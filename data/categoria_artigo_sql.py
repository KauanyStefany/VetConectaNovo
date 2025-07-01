CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS categoria_artigo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT
);
"""
INSERIR = """
INSERT INTO categoria_artigo (nome, descricao)
VALUES (?, ?);
"""
ATUALIZAR = """
UPDATE categoria_artigo SET nome = ?, descricao = ?
WHERE id = ?;
"""
EXCLUIR = """
DELETE FROM categoria_artigo 
WHERE id = ?;
"""
OBTER_TODOS_PAGINADO = """
SELECT * 
FROM categoria_artigo 
ORDER BY nome
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT * 
FROM categoria_artigo 
WHERE id = ?;
"""

