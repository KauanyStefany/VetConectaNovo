CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS comentario (
    id_comentario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_postagem_artigo INTEGER NOT NULL,
    texto TEXT NOT NULL,
    data_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_moderacao DATETIME,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_postagem_artigo) REFERENCES postagem_artigo(id_postagem_artigo)
);
"""

INSERIR = """
INSERT INTO comentario (id_usuario, id_postagem_artigo, texto)
VALUES (?, ?, ?);
"""

ATUALIZAR = """
UPDATE comentario SET texto = ?, data_moderacao = ?
WHERE id_comentario = ?;
"""

EXCLUIR = """
DELETE FROM comentario
WHERE id_comentario = ?;
"""

OBTER_PAGINA = """
SELECT
    c.id_comentario,
    c.texto,
    c.data_comentario,
    c.data_moderacao,
    c.id_usuario,
    u.nome AS nome_usuario,
    c.id_postagem_artigo,
    a.titulo AS titulo_artigo
FROM comentario c
JOIN usuario u ON c.id_usuario = u.id_usuario
JOIN postagem_artigo a ON c.id_postagem_artigo = a.id_postagem_artigo
ORDER BY c.data_comentario DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT
    c.id_comentario,
    c.texto,
    c.data_comentario,
    c.data_moderacao,
    c.id_usuario,
    u.nome AS nome_usuario,
    c.id_postagem_artigo,
    a.titulo AS titulo_artigo
FROM comentario c
JOIN usuario u ON c.id_usuario = u.id_usuario
JOIN postagem_artigo a ON c.id_postagem_artigo = a.id_postagem_artigo
WHERE c.id_comentario = ?;
"""
