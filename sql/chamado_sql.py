CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS chamado (
    id_chamado INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_admin INTEGER,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    status TEXT CHECK(status IN ('aberto', 'em_andamento', 'resolvido')) DEFAULT 'aberto',
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_admin) REFERENCES administrador(id_admin)
);
"""

INSERIR = """
INSERT INTO chamado (id_usuario, id_admin, titulo, descricao, status, data) 
VALUES (?, ?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE chamado 
SET id_usuario = ?, id_admin = ?, titulo = ?, descricao = ?, status = ?, data = ?
WHERE id_chamado = ?
"""

ATUALIZAR_STATUS = """
UPDATE chamado
SET status = ?
WHERE id_chamado = ?;
"""

EXCLUIR = """
DELETE FROM chamado
WHERE id_chamado = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT id_chamado, id_usuario, id_admin, titulo, descricao, status, data
FROM chamado
ORDER BY id_chamado
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT * 
FROM chamado
WHERE id_chamado = ?;

"""