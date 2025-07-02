CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS comentario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_artigo INTEGER NOT NULL,
    texto TEXT NOT NULL,
    data_comentario DATE DEFAULT CURRENT_DATE,
    data_moderacao DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    FOREIGN KEY (id_artigo) REFERENCES postagem_artigo(id)
);
"""
INSERIR = """
INSERT INTO comentario (id_usuario, id_artigo, texto, data_comentario, data_moderacao)
VALUES (?, ?, ?);
"""
ATUALIZAR = """
UPDATE comentario SET texto = ?, data_moderacao = ?
WHERE id = ?;
"""
EXCLUIR = """
DELETE FROM comentario 
WHERE id = ?;
"""
OBTER_TODOS_PAGINADO = """
SELECT 
    c.id,
    c.texto,
    c.data_comentario,
    c.data_moderacao,
    u.id_usuario,
    u.nome AS nome_usuario,
    a.id AS id_artigo,
    a.titulo AS titulo_artigo
FROM comentario c
JOIN usuario u ON c.id_usuario = u.id_usuario
JOIN postagem_artigo a ON c.id_artigo = a.id
ORDER BY c.data_comentario DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
    c.id,
    c.texto,
    c.data_comentario,
    c.data_moderacao,
    u.id_usuario,
    u.nome AS nome_usuario,
    a.id AS id_artigo,
    a.titulo AS titulo_artigo
FROM comentario c
JOIN usuario u ON c.id_usuario = u.id_usuario
JOIN postagem_artigo a ON c.id_artigo = a.id
WHERE c.id = ?;
"""