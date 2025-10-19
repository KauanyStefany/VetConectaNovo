CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS administrador (
    id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha CHAR(8) NOT NULL
);
"""

INSERIR = """
INSERT INTO administrador (nome, email, senha )
VALUES (?, ?, ?);
"""

ATUALIZAR = """
UPDATE administrador
SET nome = ?, email = ?, senha = ?
WHERE id_admin = ?;
"""

ATUALIZAR_SENHA = """
UPDATE administrador
SET senha = ?
WHERE id_admin = ?;
"""

EXCLUIR = """
DELETE FROM administrador
WHERE id_admin = ?;
"""

OBTER_PAGINA = """
SELECT *
FROM administrador
ORDER BY id_admin
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT *
FROM administrador
WHERE id_admin = ?;
"""

IMPORTAR = """
INSERT INTO administrador (id_admin, nome, email, senha)
VALUES (?, ?, ?, ?);
"""
