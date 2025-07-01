CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS tutor (
    id_tutor INTEGER PRIMARY KEY,
    FOREIGN KEY (id_tutor) REFERENCES usuario(id_usuario)
);
"""

INSERIR = """
INSERT INTO tutor (id_tutor)
VALUES (?);
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
    u.telefone
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
u.telefone
FROM tutor t
INNER JOIN usuario u ON t.id_usuario = u.id_usuario
WHERE t.id_tutor = ?;
"""