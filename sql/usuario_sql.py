CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    telefone TEXT NOT NULL,
    perfil TEXT NOT NULL DEFAULT 'tutor',
    foto TEXT,
    token_redefinicao TEXT,
    data_token TIMESTAMP,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, telefone, perfil)
VALUES (?, ?, ?, ?, ?);
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

OBTER_PAGINA = """
SELECT
    id_usuario,
    nome,
    email,
    senha,
    telefone,
    perfil,
    foto,
    token_redefinicao,
    data_token,
    data_cadastro
FROM usuario
ORDER BY nome
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT
id_usuario,
nome,
email,
senha,
telefone,
perfil,
foto,
token_redefinicao,
data_token,
data_cadastro
FROM usuario
WHERE id_usuario = ?;
"""

OBTER_POR_EMAIL = """
SELECT
id_usuario, nome, email, senha, telefone, perfil, foto, token_redefinicao, data_token, data_cadastro
FROM usuario
WHERE email=?
"""

ATUALIZAR_TOKEN = """
UPDATE usuario
SET token_redefinicao=?, data_token=?
WHERE email=?
"""

ATUALIZAR_FOTO = """
UPDATE usuario
SET foto = ?
WHERE id_usuario = ?
"""

OBTER_POR_TOKEN = """
SELECT
id_usuario, nome, email, senha, telefone, perfil, foto, token_redefinicao, data_token
FROM usuario
WHERE token_redefinicao=? AND data_token > datetime('now')
"""

LIMPAR_TOKEN = """
UPDATE usuario
SET token_redefinicao = NULL, data_token = NULL
WHERE id_usuario = ?;
"""

OBTER_POR_PERFIL = """
SELECT
    id_usuario, nome, email, senha, telefone, perfil,
    foto, token_redefinicao, data_token, data_cadastro
FROM usuario
WHERE perfil = ?
ORDER BY nome;
"""
