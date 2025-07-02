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
  s.id_veterinario,
  v.nome AS nome_veterinario,
  s.id_tutor,
  t.nome AS nome_tutor,
  s.data_inicio
FROM seguida s
JOIN veterinario v ON s.id_veterinario = v.id_usuario
JOIN tutor t ON s.id_tutor = t.id_usuario
ORDER BY s.data_inicio DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
  s.id_veterinario,
  v.nome AS nome_veterinario,
  s.id_tutor,
  t.nome AS nome_tutor,
  s.data_inicio
FROM seguida s
JOIN veterinario v ON s.id_veterinario = v.id_usuario
JOIN tutor t ON s.id_tutor = t.id_usuario
WHERE s.id_veterinario = ? AND s.id_tutor = ?;
"""
