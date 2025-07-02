CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS seguida (
  id_veterinario INTEGER NOT NULL,
  id_tutor INTEGER NOT NULL,
  data_inicio DATE DEFAULT CURRENT_DATE,
  PRIMARY KEY (id_veterinario, id_tutor),
  FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_veterinario),
  FOREIGN KEY (id_tutor) REFERENCES tutor(id_tutor)
);
"""

INSERIR = """
INSERT INTO seguida (id_veterinario, id_tutor)
VALUES (?, ?);
"""

EXCLUIR = """
DELETE FROM seguida 
WHERE id_veterinario = ? AND id_tutor = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
  id_veterinario,
  id_tutor,
  data_inicio
FROM seguida
ORDER BY data_inicio DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
  id_veterinario,
  id_tutor,
  data_inicio
FROM seguida
WHERE id_veterinario = ? AND id_tutor = ?;
"""
