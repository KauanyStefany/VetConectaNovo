CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS curtida_artigo (
    id_usuario INTEGER NOT NULL,
    id_postagem_artigo INTEGER NOT NULL,
    data_curtida DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario, id_postagem_artigo),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_postagem_artigo) REFERENCES postagem_artigo(id_postagem_artigo) ON DELETE CASCADE
);  
"""

INSERIR = """
INSERT INTO curtida_artigo (id_usuario, id_postagem_artigo, data_curtida)
VALUES (?, ?, ?);
"""

ATUALIZAR = """
UPDATE curtida_artigo
SET data_curtida = ?
WHERE id_usuario = ? AND id_postagem_artigo = ?;
"""

EXCLUIR = """
DELETE FROM curtida_artigo
WHERE id_usuario = ? AND id_postagem_artigo = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT
    ca.id_usuario,
    u.nome AS nome_usuario,
    u.email AS email_usuario,
    ca.id_postagem_artigo,
    pa.titulo AS titulo_artigo,
    pa.conteudo AS conteudo_artigo,
    ca.data_curtida
FROM curtida_artigo ca
INNER JOIN usuario u ON ca.id_usuario = u.id_usuario
INNER JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id_postagem_artigo
ORDER BY ca.data_curtida DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT
    ca.id_usuario,
    u.nome AS nome_usuario,
    u.email AS email_usuario,
    ca.id_postagem_artigo,
    pa.titulo AS titulo_artigo,
    pa.conteudo AS conteudo_artigo,
    ca.data_curtida
FROM curtida_artigo ca
INNER JOIN usuario u ON ca.id_usuario = u.id_usuario
INNER JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id_postagem_artigo
WHERE ca.id_usuario = ? AND ca.id_postagem_artigo = ?;
"""

CONTAR_CURTIDAS_POR_ARTIGO = """
SELECT COUNT(*) as total_curtidas
FROM curtida_artigo
WHERE id_postagem_artigo = ?;
"""

CONTAR_CURTIDAS_POR_USUARIO = """
SELECT COUNT(*) as total_curtidas
FROM curtida_artigo
WHERE id_usuario = ?;
"""

VERIFICAR_CURTIDA_EXISTE = """
SELECT 1
FROM curtida_artigo
WHERE id_usuario = ? AND id_postagem_artigo = ?
LIMIT 1;
"""

OBTER_ARTIGOS_CURTIDOS_POR_USUARIO = """
SELECT
    ca.id_usuario,
    u.nome AS nome_usuario,
    ca.id_postagem_artigo,
    pa.titulo AS titulo_artigo,
    pa.conteudo AS conteudo_artigo,
    ca.data_curtida
FROM curtida_artigo ca
INNER JOIN usuario u ON ca.id_usuario = u.id_usuario
INNER JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id_postagem_artigo
WHERE ca.id_usuario = ?
ORDER BY ca.data_curtida DESC
LIMIT ? OFFSET ?;
"""