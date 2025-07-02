CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS veterinario (
    id_veterinario INTEGER PRIMARY KEY,
    crmv TEXT NOT NULL,
    verificado BOOLEAN DEFAULT 0,
    bio TEXT,
    FOREIGN KEY (id_veterinario) REFERENCES usuario(id_usuario)
);
"""

INSERIR = """
INSERT INTO veterinario (id_veterinario, crmv, verificado, bio)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE veterinario SET crmv = ?, verificado = ?, bio = ?
WHERE id_veterinario = ?;
"""

EXCLUIR = """
DELETE FROM veterinario 
WHERE id_veterinario = ?;
"""

OBTER_VETERINARIO_PAGINADO = """
SELECT
    v.id_veterinario,
    u.nome,
    u.email,
    u.telefone,
    v.crmv,
    v.bio
FROM veterinario v
INNER JOIN usuario u ON v.id_veterinario = u.id_usuario
ORDER BY v.id_veterinario
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT 
    v.id_veterinario,
    u.nome,
    u.email,
    u.senha,
    u.telefone,
    v.crmv,
    v.verificado,
    v.bio
FROM veterinario v
JOIN usuario u ON v.id_usuario = u.id_usuario
WHERE v.id_veterinario = ?
"""

