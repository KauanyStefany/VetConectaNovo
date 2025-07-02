CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS curtida_feed (
    id_usuario INTEGER NOT NULL,
    id_postagem_feed INTEGER NOT NULL,
    data_curtida DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id_usuario, id_postagem_feed),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_postagem_feed) REFERENCES postagem_feed(id_postagem_feed)
);
"""

INSERIR = """
INSERT INTO curtida_feed (id_usuario, id_postagem_feed)
VALUES (?, ?);
"""

EXCLUIR = """
DELETE FROM curtida_feed 
WHERE id_usuario = ? AND id_postagem_feed = ?;
"""


OBTER_TODOS_PAGINADO = """
SELECT 
    cf.id_usuario,
    u.nome AS nome_usuario,
    cf.id_postagem_feed,
    pf.descricao AS descricao_postagem,
    pf.imagem,
    cf.data_curtida
FROM curtida_feed cf
JOIN usuario u ON cf.id_usuario = u.id_usuario
JOIN postagem_feed pf ON cf.id_postagem_feed = pf.id_postagem_feed
ORDER BY cf.data_curtida DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT 
    u.nome AS nome_usuario,
    pf.descricao AS descricao_postagem,
    pf.imagem,
    cf.data_curtida
FROM curtida_feed cf
JOIN usuario u ON cf.id_usuario = u.id_usuario
JOIN postagem_feed pf ON cf.id_postagem_feed = pf.id_postagem_feed
WHERE cf.id_usuario = ? AND cf.id_postagem_feed = ?;
"""
