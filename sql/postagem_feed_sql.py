CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS postagem_feed (
    id_postagem_feed INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tutor INTEGER NOT NULL,
    descricao TEXT,
    data_postagem DATETIME DEFAULT CURRENT_TIMESTAMP,
    visualizacoes INTEGER DEFAULT 0,
    FOREIGN KEY (id_tutor) REFERENCES tutor(id_tutor)

);
"""

INSERIR = """
INSERT INTO postagem_feed (id_tutor, descricao)
VALUES (?, ?);
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

OBTER_PAGINA = """
SELECT
    id_postagem_feed,
    id_tutor,
    descricao,
    data_postagem,
    visualizacoes
FROM postagem_feed
ORDER BY data_postagem DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT
    id_postagem_feed,
    id_tutor,
    descricao,
    data_postagem,
    visualizacoes
FROM postagem_feed
WHERE id_postagem_feed = ?;
"""

INCREMENTAR_VISUALIZACOES = """
UPDATE postagem_feed
SET visualizacoes = visualizacoes + 1
WHERE id_postagem_feed = ?;
"""

IMPORTAR = """
INSERT INTO postagem_feed (id_postagem_feed, id_tutor, descricao, data_postagem, visualizacoes)
VALUES (?, ?, ?, ?, ?);
"""

OBTER_RECENTES_COM_DADOS = """
SELECT
    pf.id_postagem_feed,
    pf.id_tutor,
    pf.descricao,
    pf.data_postagem,
    pf.visualizacoes,
    u.nome as nome_tutor,
    t.quantidade_pets
FROM postagem_feed pf
JOIN tutor t ON pf.id_tutor = t.id_tutor
JOIN usuario u ON t.id_tutor = u.id_usuario
ORDER BY pf.data_postagem DESC
LIMIT ?;
"""

OBTER_PAGINA_COM_DADOS = """
SELECT
    pf.id_postagem_feed,
    pf.id_tutor,
    pf.descricao,
    pf.data_postagem,
    pf.visualizacoes,
    u.nome as nome_tutor,
    t.quantidade_pets
FROM postagem_feed pf
JOIN tutor t ON pf.id_tutor = t.id_tutor
JOIN usuario u ON t.id_tutor = u.id_usuario
ORDER BY pf.data_postagem DESC
LIMIT ? OFFSET ?;
"""

CONTAR_TOTAL = """
SELECT COUNT(*) as total
FROM postagem_feed;
"""

OBTER_POR_ID_COM_DADOS = """
SELECT
    pf.id_postagem_feed,
    pf.id_tutor,
    pf.descricao,
    pf.data_postagem,
    pf.visualizacoes,
    u.id_usuario,
    u.nome as nome_tutor,
    u.email as email_tutor,
    u.telefone as telefone_tutor,
    t.quantidade_pets
FROM postagem_feed pf
JOIN tutor t ON pf.id_tutor = t.id_tutor
JOIN usuario u ON t.id_tutor = u.id_usuario
WHERE pf.id_postagem_feed = ?;
"""
