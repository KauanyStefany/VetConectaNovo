CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS postagem_feed (
    id_postagem_feed INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tutor INTEGER NOT NULL,
    imagem TEXT,
    descricao TEXT,
    data_postagem DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_tutor) REFERENCES tutor(id_usuario)
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
    pf.id_postagem_feed,
    pf.id_tutor,
    u.nome AS nome_tutor,
    pf.imagem,
    pf.descricao,
    pf.data_postagem
FROM postagem_feed pf
JOIN tutor t ON pf.id_tutor = t.id_usuario
JOIN usuario u ON t.id_usuario = u.id_usuario
ORDER BY pf.data_postagem DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
    pf.id_postagem_feed,
    pf.id_tutor,
    u.nome AS nome_tutor,
    pf.imagem,
    pf.descricao,
    pf.data_postagem
FROM postagem_feed pf
JOIN tutor t ON pf.id_tutor = t.id_usuario
JOIN usuario u ON t.id_usuario = u.id_usuario
WHERE pf.id_postagem_feed = ?;
"""
