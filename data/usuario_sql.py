CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha CHAR(8) NOT NULL,
    telefone CHAR(11) NOT NULL
);
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, telefone)
VALUES (?, ?, ?, ?);
"""
ATUALIZAR = """
UPDATE usuario 
SET nome = ?, email = ?, telefone = ?
WHERE id_usuario = ?;
"""

ATUALIZAR_SENHA = """
UPDATE usuario 
SET senha = ?
WHERE id_usuario = ?;
"""

EXCLUIR = """
DELETE FROM usuario 
WHERE id_usuario = ?;
"""
OBTER_TODOS_PAGINADO = """
SELECT 
    id_usuario, 
    nome, 
    email, 
    senha, 
    telefone
FROM usuario 
ORDER BY nome
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
id_usuario, 
nome, 
email, 
telefone
FROM usuario 
WHERE id_usuario = ?;
"""