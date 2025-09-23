import os
import sys
import time
from app.database.models.categoria_artigo_model import CategoriaArtigo
from app.database.models.comentario_model import Comentario
from app.database.repositories.comentario_repo import *
from app.database.repositories.usuario_repo import criar_tabela_usuario, inserir_usuario
from app.database.models.usuario_model import Usuario
from app.database.models.veterinario_model import Veterinario
from app.database.models.postagem_artigo_model import PostagemArtigo

def unique_email(prefix="test"):
    """Gera um email único para testes"""
    timestamp = str(int(time.time() * 1000000))
    return f"{prefix}_{timestamp}@test.com"

from app.database.repositories.comentario_repo import inserir
from app.database.repositories.comentario_repo import inserir, obter_por_id, criar_tabela as criar_tabela_comentario
from app.database.repositories.usuario_repo import inserir_usuario, criar_tabela_usuario
from app.database.repositories.veterinario_repo import criar_tabela_veterinario
from app.database.repositories.categoria_artigo_repo import inserir_categoria, criar_tabela_categoria_artigo
from app.database.repositories.postagem_artigo_repo import inserir as inserir_artigo, criar_tabela as criar_tabela_postagem_artigo
from app.database.repositories.veterinario_repo import inserir_veterinario
from datetime import datetime


class TestComentarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela de comentários deveria retornar True"

    def test_inserir(self, test_db):
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_postagem_artigo()  
        criar_tabela_comentario()
        
        usuario_teste = Usuario(id_usuario=0, nome="Usuário Teste", email=unique_email("usuario"), senha="senha123", telefone="11999999999")
        id_usuario = inserir_usuario(usuario_teste)
        usuario_teste.id_usuario = id_usuario  # Atualiza o ID do usuário após inserção
        
        # Criar veterinário diretamente (inserir_veterinario já cria o usuário)
        veterinario_teste = Veterinario(
            id_usuario=0,
            nome="Veterinário Teste",
            email=unique_email("veterinario"),  # Email único
            senha="senha123",
            telefone="11888888888",
            crmv="CRMV12345",
            verificado=True,
            bio="bioteste"
        )
        id_usuario_vet = inserir_veterinario(veterinario_teste)
        veterinario_teste.id_usuario = id_usuario_vet
    
        categoria_artigo_teste = CategoriaArtigo(0, "Categoria Teste", "Descrição da categoria teste")
        id_categoria_artigo = inserir_categoria(categoria_artigo_teste)
        categoria_artigo_teste.id = id_categoria_artigo
        
        postagem_artigo_teste = PostagemArtigo(
            id_postagem_artigo=0,
            id_veterinario=id_usuario_vet,  # ID do veterinário
            titulo="Título do Artigo Teste",
            conteudo="Conteúdo do artigo teste",
            id_categoria_artigo=id_categoria_artigo,  # ID da categoria
            data_publicacao="2023-10-01",
            visualizacoes=100  # inteiro, não string
        )
        id_postagem_artigo = inserir_artigo(postagem_artigo_teste)
        postagem_artigo_teste.id_postagem_artigo = id_postagem_artigo
        
        comentario_teste = Comentario(
            id_comentario=0,
            id_usuario=id_usuario,  # ID do usuário
            id_postagem_artigo=id_postagem_artigo,  # ID da postagem
            texto="Este é um comentário de teste",
            data_comentario=datetime.now(),
            data_moderacao=None
        )
        
        id_comentario_inserido = inserir(comentario_teste)
        
        comentario_db = obter_por_id(id_comentario_inserido)
        
        # ASSERTS
        assert comentario_db is not None, "O comentário inserido não deveria ser None"
        assert comentario_db.id_usuario == id_usuario, "O ID do usuário do comentário inserido não confere"
        assert comentario_db.id_postagem_artigo == id_postagem_artigo, "O ID do artigo do comentário inserido não confere"
        assert comentario_db.texto == "Este é um comentário de teste", "O texto do comentário inserido não confere"
