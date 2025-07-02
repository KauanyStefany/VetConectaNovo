# 

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS postagem_artigo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_veterinario INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    id_categoria_artigo INTEGER NOT NULL,
    data_publicacao DATE DEFAULT CURRENT_DATE,
    visualizacoes INTEGER DEFAULT 0,
    FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_usuario),
    FOREIGN KEY (id_categoria_artigo) REFERENCES categoria_artigo(id)
);
"""

INSERIR = """
INSERT INTO postagem_artigo (id_veterinario, titulo, conteudo, id_categoria_artigo)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE postagem_artigo 
SET titulo = ?, conteudo = ?, id_categoria_artigo = ?, visualizacoes = ?
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM postagem_artigo 
WHERE id = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
    p.id,
    p.id_veterinario,
    v.nome AS nome_veterinario,
    v.email AS email_veterinario,
    v.senha AS senha_veterinario,
    v.telefone AS telefone_veterinario,
    v.crmv AS crmv_veterinario,
    v.verificado AS verificado_veterinario,
    v.bio AS bio_veterinario,
    p.titulo,
    p.conteudo,
    p.id_categoria_artigo,
    c.nome AS nome_categoria,
    c.descricao AS descricao_categoria,
    p.data_publicacao,
    p.visualizacoes
FROM postagem_artigo p
JOIN categoria_artigo c ON p.id_categoria_artigo = c.id
JOIN veterinario v ON p.id_veterinario = v.id_usuario
ORDER BY p.data_publicacao DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT 
    p.id,
    p.id_veterinario,
    v.nome AS nome_veterinario,
    v.email AS email_veterinario,
    v.senha AS senha_veterinario,
    v.telefone AS telefone_veterinario,
    v.crmv AS crmv_veterinario,
    v.verificado AS verificado_veterinario,
    v.bio AS bio_veterinario,
    p.titulo,
    p.conteudo,
    p.id_categoria_artigo,
    c.nome AS nome_categoria,
    c.descricao AS descricao_categoria,
    p.data_publicacao,
    p.visualizacoes
FROM postagem_artigo p
JOIN categoria_artigo c ON p.id_categoria_artigo = c.id
JOIN veterinario v ON p.id_veterinario = v.id_usuario
WHERE p.id = ?;
"""