"""
Pacote de repositórios para acesso a dados.
Re-exporta repositórios para facilitar imports.
"""

# Importar repos originais para manter compatibilidade
from repo import (
    administrador_repo,
    categoria_artigo_repo,
    chamado_repo,
    comentario_repo,
    curtida_artigo_repo,
    curtida_feed_repo,
    denuncia_repo,
    postagem_artigo_repo,
    postagem_feed_repo,
    resposta_chamado_repo,
    seguida_repo,
    tutor_repo,
    usuario_repo,
    verificacao_crmv_repo,
    veterinario_repo
)

__all__ = [
    'administrador_repo',
    'categoria_artigo_repo',
    'chamado_repo',
    'comentario_repo',
    'curtida_artigo_repo',
    'curtida_feed_repo',
    'denuncia_repo',
    'postagem_artigo_repo',
    'postagem_feed_repo',
    'resposta_chamado_repo',
    'seguida_repo',
    'tutor_repo',
    'usuario_repo',
    'verificacao_crmv_repo',
    'veterinario_repo'
]
