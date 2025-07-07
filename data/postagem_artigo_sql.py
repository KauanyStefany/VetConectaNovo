CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS postagem_artigo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_veterinario INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    id_categoria_artigo INTEGER NOT NULL,
    data_publicacao DATE DEFAULT CURRENT_DATE,
    visualizacoes INTEGER DEFAULT 0,
    FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_veterinario),
    FOREIGN KEY (id_categoria_artigo) REFERENCES categoria_artigo(id)
);
"""

INSERIR = """
INSERT INTO postagem_artigo (id_veterinario, titulo, conteudo, id_categoria_artigo)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE postagem_artigo 
SET titulo = ?, conteudo = ?, id_categoria_artigo = ?
WHERE id = ?;
"""

INCREMENTAR_VISUALIZACOES = """
UPDATE postagem_artigo
SET visualizacoes = visualizacoes + 1
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM postagem_artigo 
WHERE id = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
    id,
    id_veterinario,
    titulo,
    conteudo,
    id_categoria_artigo,
    data_publicacao,
    visualizacoes
FROM postagem_artigo
ORDER BY data_publicacao DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT 
    id,
    id_veterinario,
    titulo,
    conteudo,
    id_categoria_artigo,
    data_publicacao,
    visualizacoes
FROM postagem_artigo
WHERE id = ?;
"""