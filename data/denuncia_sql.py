CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS denuncia (
    id_denuncia INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_admin INTEGER,
    motivo TEXT NOT NULL,
    data_denuncia DATETIME DEFAULT CURRENT_DATE,
    status TEXT NOT NULL CHECK (status IN ('pendente', 'aprovada', 'rejeitada')),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_admin) REFERENCES administrador(id_admin)
);
"""

INSERIR = """
INSERT INTO denuncia (id_usuario, id_admin, motivo, status)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE denuncia 
SET id_usuario = ?, id_admin = ?, motivo = ?, status = ?
WHERE id_denuncia = ?;
"""

EXCLUIR = """
DELETE FROM denuncia 
WHERE id_denuncia = ?;
"""

OBTER_TODAS_DENUNCIAS_PAGINADAS = """
SELECT
    d.id_denuncia,
    d.id_usuario,
    u.nome AS nome_usuario,
    d.id_admin,
    a.nome AS nome_admin,
    d.motivo,
    d.data_denuncia,
    d.status
FROM denuncia d
INNER JOIN usuario u ON d.id_usuario = u.id_usuario
INNER JOIN administrador a ON d.id_admin = a.id_admin
ORDER BY d.data_denuncia DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT
    d.id_denuncia,
    d.id_usuario,
    u.nome AS nome_usuario,
    d.id_admin,
    a.nome AS nome_admin,
    d.motivo,
    d.data_denuncia,
    d.status
FROM denuncia d
INNER JOIN usuario u ON d.id_usuario = u.id_usuario
INNER JOIN administrador a ON d.id_admin = a.id_admin
WHERE d.id_denuncia = ?;
"""