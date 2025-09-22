CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS postagem_feed (
    id_postagem_feed INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tutor INTEGER NOT NULL,
    imagem TEXT,
    descricao TEXT,
    data_postagem DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_tutor) REFERENCES tutor(id_tutor)

);
"""

INSERIR = """
INSERT INTO postagem_feed (id_tutor, imagem, descricao)
VALUES (?, ?, ?);
"""

ATUALIZAR = """
UPDATE postagem_feed
SET descricao = ?
WHERE id_postagem_feed = ?;
"""

EXCLUIR = """
DELETE FROM postagem_feed
WHERE id_postagem_feed = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
    id_postagem_feed,
    id_tutor,    
    imagem,
    descricao,
    data_postagem
FROM postagem_feed
ORDER BY data_postagem DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT 
    id_postagem_feed,
    id_tutor,
    imagem,
    descricao,
    data_postagem
FROM postagem_feed
WHERE id_postagem_feed = ?;
"""
