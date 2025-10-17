CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS verificacao_crmv (
    id_verificacao_crmv INTEGER PRIMARY KEY AUTOINCREMENT,
    id_veterinario INTEGER NOT NULL,
    id_administrador INTEGER,
    data_verificacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_verificacao TEXT CHECK(status_verificacao IN ('pendente', 'aprovado', 'rejeitado', 'em_analise')) DEFAULT 'pendente'
);
"""

INSERIR = """
INSERT INTO verificacao_crmv (id_veterinario, id_administrador, status_verificacao)
VALUES (?, ?, ?);
"""

ATUALIZAR = """
UPDATE verificacao_crmv
SET status_verificacao = ?, id_administrador = ?
WHERE id_veterinario = ?;
"""

EXCLUIR = """
DELETE FROM verificacao_crmv
WHERE id_veterinario = ?;
"""

OBTER_PAGINA = """
SELECT
    v.id_verificacao_crmv,
    v.data_verificacao,
    v.status_verificacao,
    u.id_usuario AS id_veterinario,
    u.nome AS nome_veterinario,
    u.email AS email_veterinario,
    u.telefone AS telefone_veterinario,
    vet.crmv,
    vet.verificado AS veterinario_verificado,
    vet.bio AS bio_veterinario,
    a.id_admin,
    a.nome AS nome_admin,
    a.email AS email_admin
FROM verificacao_crmv v
JOIN usuario u ON v.id_veterinario = u.id_usuario
JOIN veterinario vet ON v.id_veterinario = vet.id_veterinario
LEFT JOIN administrador a ON v.id_administrador = a.id_admin
ORDER BY v.data_verificacao DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT
    v.id_verificacao_crmv,
    v.data_verificacao,
    v.status_verificacao,
    u.id_usuario AS id_veterinario,
    u.nome AS nome_veterinario,
    u.email AS email_veterinario,
    u.telefone AS telefone_veterinario,
    vet.crmv,
    vet.verificado AS veterinario_verificado,
    vet.bio AS bio_veterinario,
    a.id_admin,
    a.nome AS nome_admin,
    a.email AS email_admin,
    a.senha AS senha_admin

FROM verificacao_crmv v
JOIN usuario u ON v.id_veterinario = u.id_usuario
JOIN veterinario vet ON v.id_veterinario = vet.id_veterinario
LEFT JOIN administrador a ON v.id_administrador = a.id_admin
WHERE v.id_verificacao_crmv = ?;
"""
