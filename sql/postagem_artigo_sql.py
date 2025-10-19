CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS postagem_artigo (
    id_postagem_artigo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_veterinario INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    id_categoria_artigo INTEGER NOT NULL,
    data_publicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    visualizacoes INTEGER DEFAULT 0,
    FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_veterinario),
    FOREIGN KEY (id_categoria_artigo) REFERENCES categoria_artigo(id_categoria_artigo)
);
"""

INSERIR = """
INSERT INTO postagem_artigo (id_veterinario, titulo, conteudo, id_categoria_artigo)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE postagem_artigo
SET titulo = ?, conteudo = ?, id_categoria_artigo = ?
WHERE id_postagem_artigo = ?;
"""

INCREMENTAR_VISUALIZACOES = """
UPDATE postagem_artigo
SET visualizacoes = visualizacoes + 1
WHERE id_postagem_artigo = ?;
"""

EXCLUIR = """
DELETE FROM postagem_artigo
WHERE id_postagem_artigo = ?;
"""

OBTER_PAGINA = """
SELECT
    id_postagem_artigo,
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
    id_postagem_artigo,
    id_veterinario,
    titulo,
    conteudo,
    id_categoria_artigo,
    data_publicacao,
    visualizacoes
FROM postagem_artigo
WHERE id_postagem_artigo = ?;
"""

OBTER_RECENTES_COM_DADOS = """
SELECT
    pa.id_postagem_artigo,
    pa.id_veterinario,
    pa.titulo,
    pa.conteudo,
    pa.id_categoria_artigo,
    pa.data_publicacao,
    pa.visualizacoes,
    u.nome as nome_veterinario,
    ca.nome as nome_categoria,
    ca.cor as cor_categoria
FROM postagem_artigo pa
JOIN veterinario v ON pa.id_veterinario = v.id_veterinario
JOIN usuario u ON v.id_veterinario = u.id_usuario
JOIN categoria_artigo ca ON pa.id_categoria_artigo = ca.id_categoria_artigo
ORDER BY pa.data_publicacao DESC
LIMIT ?;
"""

OBTER_PAGINA_COM_DADOS = """
SELECT
    pa.id_postagem_artigo,
    pa.id_veterinario,
    pa.titulo,
    pa.conteudo,
    pa.id_categoria_artigo,
    pa.data_publicacao,
    pa.visualizacoes,
    u.nome as nome_veterinario,
    ca.nome as nome_categoria,
    ca.cor as cor_categoria
FROM postagem_artigo pa
JOIN veterinario v ON pa.id_veterinario = v.id_veterinario
JOIN usuario u ON v.id_veterinario = u.id_usuario
JOIN categoria_artigo ca ON pa.id_categoria_artigo = ca.id_categoria_artigo
ORDER BY pa.data_publicacao DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_CATEGORIA_COM_DADOS = """
SELECT
    pa.id_postagem_artigo,
    pa.id_veterinario,
    pa.titulo,
    pa.conteudo,
    pa.id_categoria_artigo,
    pa.data_publicacao,
    pa.visualizacoes,
    u.nome as nome_veterinario,
    ca.nome as nome_categoria,
    ca.cor as cor_categoria
FROM postagem_artigo pa
JOIN veterinario v ON pa.id_veterinario = v.id_veterinario
JOIN usuario u ON v.id_veterinario = u.id_usuario
JOIN categoria_artigo ca ON pa.id_categoria_artigo = ca.id_categoria_artigo
WHERE pa.id_categoria_artigo = ?
ORDER BY pa.data_publicacao DESC
LIMIT ? OFFSET ?;
"""

IMPORTAR = """
INSERT INTO postagem_artigo (id_postagem_artigo, id_veterinario, titulo, conteudo, id_categoria_artigo, visualizacoes)
VALUES (?, ?, ?, ?, ?, ?);
"""
