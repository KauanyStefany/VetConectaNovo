CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS curtida_artigo (
    id_usuario INTEGER NOT NULL,
    id_postagem_artigo INTEGER NOT NULL,
    data_curtida DATE DEFAULT CURRENT_DATE
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
INNER JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id
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
INNER JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id
WHERE ca.id_usuario = ? AND ca.id_postagem_artigo = ?;
"""