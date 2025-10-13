CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS tutor (
    id_tutor INTEGER PRIMARY KEY,
    quantidade_pets INTEGER DEFAULT 0,
    descricao_pets TEXT,
    FOREIGN KEY (id_tutor) REFERENCES usuario(id_usuario)
);
"""

INSERIR = """
INSERT INTO tutor (id_tutor, quantidade_pets, descricao_pets)
VALUES (?, ?, ?);
"""

ATUALIZAR = """
UPDATE tutor 
SET quantidade_pets = ?, descricao_pets = ?
WHERE id_tutor = ?;
"""

EXCLUIR = """
DELETE FROM tutor 
WHERE id_tutor = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
    t.id_tutor,
    u.nome, 
    u.email, 
    u.telefone,
    t.quantidade_pets,
    t.descricao_pets
FROM tutor t
INNER JOIN usuario u ON t.id_tutor = u.id_usuario
ORDER BY u.nome
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT 
    t.id_tutor,
    u.nome,
    u.email,
    u.telefone,
    u.perfil,
    u.foto,
    u.token_redefinicao,
    u.data_token,
    u.data_cadastro,
    t.quantidade_pets,
    t.descricao_pets
FROM tutor t
INNER JOIN usuario u ON t.id_tutor = u.id_usuario
WHERE t.id_tutor = ?;
"""