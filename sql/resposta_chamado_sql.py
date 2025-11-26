CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS resposta_chamado (
    id_resposta_chamado INTEGER PRIMARY KEY AUTOINCREMENT,
    id_chamado INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_chamado) REFERENCES chamado(id_chamado)
);
"""

INSERIR = """
INSERT INTO resposta_chamado (id_chamado, titulo, descricao, data)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE resposta_chamado
SET id_chamado = ?, titulo = ?, descricao = ?, data = ?
WHERE id_resposta_chamado = ?;
"""


EXCLUIR = """
DELETE FROM resposta_chamado
WHERE id_resposta_chamado = ?;
"""

OBTER_PAGINA = """
SELECT *
FROM resposta_chamado
ORDER BY data DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT *
FROM resposta_chamado
WHERE id_resposta_chamado = ?;
"""

OBTER_POR_CHAMADO = """
SELECT id_resposta_chamado, id_chamado, titulo, descricao, data
FROM respostas_chamado
WHERE id_chamado = ?
ORDER BY data ASC
"""
