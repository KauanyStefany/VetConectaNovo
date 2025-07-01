CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS chamado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_admin INTEGER,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    status TEXT CHECK(status IN ('aberto', 'em andamento', 'resolvido')) DEFAULT 'aberto',
    data DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
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
WHERE id = ?
"""

EXCLUIR = """
DELETE FROM chamado
WHERE id = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT * 
FROM chamado 
ORDER BY data DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT * 
FROM chamado
WHERE id = ?;

"""