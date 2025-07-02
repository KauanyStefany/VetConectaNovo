CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS resposta_chamado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_chamado INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_chamado) REFERENCES chamado(id)
);
"""

INSERIR = """
INSERT INTO resposta_chamado (id_chamado, titulo, descricao, data) 
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE resposta_chamado 
SET id_chamado = ?, titulo = ?, descricao = ?, data = ?
WHERE id = ?;
"""


EXCLUIR = """
DELETE FROM resposta_chamado
WHERE id = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT * 
FROM resposta_chamado 
ORDER BY data DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT * 
FROM resposta_chamado
WHERE id = ?;

"""