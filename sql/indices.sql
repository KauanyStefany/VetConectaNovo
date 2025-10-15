-- Script de criação de índices para otimização de performance
-- Gerado em: 2025-10-15
-- VetConecta - Sistema de Conexão Veterinária

-- =====================================================================
-- ÍNDICES PARA TABELA USUARIO
-- =====================================================================

-- Índice para busca por email (usado em autenticação)
CREATE INDEX IF NOT EXISTS idx_usuario_email ON usuario(email);

-- Índice para busca por perfil (usado em listagens)
CREATE INDEX IF NOT EXISTS idx_usuario_perfil ON usuario(perfil);

-- Índice para busca por token de redefinição de senha
CREATE INDEX IF NOT EXISTS idx_usuario_token ON usuario(token_redefinicao);

-- Índice para ordenação por data de cadastro
CREATE INDEX IF NOT EXISTS idx_usuario_data_cadastro ON usuario(data_cadastro DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA VETERINARIO
-- =====================================================================

-- Índice para busca por CRMV
CREATE INDEX IF NOT EXISTS idx_veterinario_crmv ON veterinario(crmv);

-- Índice para filtro por veterinários verificados
CREATE INDEX IF NOT EXISTS idx_veterinario_verificado ON veterinario(verificado);

-- =====================================================================
-- ÍNDICES PARA TABELA TUTOR
-- =====================================================================

-- Índice para busca rápida de tutores
CREATE INDEX IF NOT EXISTS idx_tutor_id ON tutor(id_tutor);

-- =====================================================================
-- ÍNDICES PARA TABELA POSTAGEM_ARTIGO
-- =====================================================================

-- Índice para busca de postagens por veterinário
CREATE INDEX IF NOT EXISTS idx_postagem_veterinario ON postagem_artigo(id_veterinario);

-- Índice para busca de postagens por categoria
CREATE INDEX IF NOT EXISTS idx_postagem_categoria ON postagem_artigo(id_categoria_artigo);

-- Índice para ordenação por data de publicação
CREATE INDEX IF NOT EXISTS idx_postagem_data ON postagem_artigo(data_publicacao DESC);

-- Índice para ordenação por visualizações
CREATE INDEX IF NOT EXISTS idx_postagem_visualizacoes ON postagem_artigo(visualizacoes DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA POSTAGEM_FEED
-- =====================================================================

-- Índice para busca de postagens do feed por tutor
CREATE INDEX IF NOT EXISTS idx_postagem_feed_tutor ON postagem_feed(id_tutor);

-- Índice para ordenação por data de postagem
CREATE INDEX IF NOT EXISTS idx_postagem_feed_data ON postagem_feed(data_postagem DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA COMENTARIO
-- =====================================================================

-- Índice para busca de comentários por usuário
CREATE INDEX IF NOT EXISTS idx_comentario_usuario ON comentario(id_usuario);

-- Índice para busca de comentários por postagem de artigo
CREATE INDEX IF NOT EXISTS idx_comentario_postagem ON comentario(id_postagem_artigo);

-- Índice para ordenação por data de comentário
CREATE INDEX IF NOT EXISTS idx_comentario_data ON comentario(data_comentario DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA CURTIDA_ARTIGO
-- =====================================================================

-- Índice para contagem de curtidas por postagem
CREATE INDEX IF NOT EXISTS idx_curtida_artigo_postagem ON curtida_artigo(id_postagem_artigo);

-- Índice para busca de curtidas por usuário
CREATE INDEX IF NOT EXISTS idx_curtida_artigo_usuario ON curtida_artigo(id_usuario);

-- Índice para ordenação por data de curtida
CREATE INDEX IF NOT EXISTS idx_curtida_artigo_data ON curtida_artigo(data_curtida DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA CURTIDA_FEED
-- =====================================================================

-- Índice para contagem de curtidas por postagem do feed
CREATE INDEX IF NOT EXISTS idx_curtida_feed_postagem ON curtida_feed(id_postagem_feed);

-- Índice para busca de curtidas por usuário
CREATE INDEX IF NOT EXISTS idx_curtida_feed_usuario ON curtida_feed(id_usuario);

-- Índice para ordenação por data de curtida
CREATE INDEX IF NOT EXISTS idx_curtida_feed_data ON curtida_feed(data_curtida DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA SEGUIDA
-- =====================================================================

-- Índice para busca de seguidores de um veterinário
CREATE INDEX IF NOT EXISTS idx_seguida_veterinario ON seguida(id_veterinario);

-- Índice para busca de veterinários seguidos por um tutor
CREATE INDEX IF NOT EXISTS idx_seguida_tutor ON seguida(id_tutor);

-- Índice composto para verificar relacionamento seguida
CREATE INDEX IF NOT EXISTS idx_seguida_tutor_veterinario ON seguida(id_tutor, id_veterinario);

-- =====================================================================
-- ÍNDICES PARA TABELA CHAMADO
-- =====================================================================

-- Índice para busca de chamados por usuário
CREATE INDEX IF NOT EXISTS idx_chamado_usuario ON chamado(id_usuario);

-- Índice para busca de chamados por administrador
CREATE INDEX IF NOT EXISTS idx_chamado_admin ON chamado(id_admin);

-- Índice para filtro por status
CREATE INDEX IF NOT EXISTS idx_chamado_status ON chamado(status);

-- Índice para ordenação por data
CREATE INDEX IF NOT EXISTS idx_chamado_data ON chamado(data DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA RESPOSTA_CHAMADO
-- =====================================================================

-- Índice para busca de respostas por chamado
CREATE INDEX IF NOT EXISTS idx_resposta_chamado ON resposta_chamado(id_chamado);

-- Índice para ordenação por data
CREATE INDEX IF NOT EXISTS idx_resposta_data ON resposta_chamado(data DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA DENUNCIA
-- =====================================================================

-- Índice para busca de denúncias por usuário
CREATE INDEX IF NOT EXISTS idx_denuncia_usuario ON denuncia(id_usuario);

-- Índice para filtro por status
CREATE INDEX IF NOT EXISTS idx_denuncia_status ON denuncia(status);

-- Índice para ordenação por data de denúncia
CREATE INDEX IF NOT EXISTS idx_denuncia_data ON denuncia(data_denuncia DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA VERIFICACAO_CRMV
-- =====================================================================

-- Índice para busca de verificações por veterinário
CREATE INDEX IF NOT EXISTS idx_verificacao_crmv_veterinario ON verificacao_crmv(id_veterinario);

-- Índice para filtro por status de verificação
CREATE INDEX IF NOT EXISTS idx_verificacao_crmv_status ON verificacao_crmv(status_verificacao);

-- Índice para ordenação por data de verificação
CREATE INDEX IF NOT EXISTS idx_verificacao_crmv_data ON verificacao_crmv(data_verificacao DESC);

-- =====================================================================
-- ÍNDICES PARA TABELA CATEGORIA_ARTIGO
-- =====================================================================

-- Índice para ordenação por nome
CREATE INDEX IF NOT EXISTS idx_categoria_artigo_nome ON categoria_artigo(nome);

-- =====================================================================
-- FIM DO SCRIPT
-- =====================================================================
