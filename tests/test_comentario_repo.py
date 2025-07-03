import os
import sys
from data.categoria_artigo_model import CategoriaArtigo
from data.comentario_model import Comentario
from data.comentario_repo import *
from data.usuario_repo import criar_tabela_usuario, inserir_usuario
from data.usuario_model import Usuario
from data.veterinario_model import Veterinario
from data.postagem_artigo_model import PostagemArtigo

from data.comentario_repo import inserir
from data.comentario_repo import inserir, obter_por_id, criar_tabela as criar_tabela_comentario
from data.usuario_repo import inserir_usuario, criar_tabela_usuario
from data.veterinario_repo import criar_tabela_veterinario
from data.categoria_artigo_repo import inserir_categoria, criar_tabela_categoria_artigo
from data.postagem_artigo_repo import inserir as inserir_artigo, criar_tabela as criar_tabela_postagem_artigo
from data.veterinario_repo import inserir_veterinario
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
        
        usuario_teste = Usuario(0, "Usuário Teste", "usuario@teste.com", "senha123", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)
        usuario_teste.id_usuario = id_usuario  # Atualiza o ID do usuário após inserção
        
        usuario_vet = Usuario(
            id_usuario=0,
            nome="Veterinário Teste",
            email="veterinarioo@teste.com",  # ⚠️ Use email único
            senha="senha123",
            telefone="11999999999"
        )
        id_usuario_vet = inserir_usuario(usuario_vet)
        usuario_vet.id_usuario = id_usuario_vet

        
        veterinario_teste = Veterinario(
            id_usuario=id_usuario_vet,
            nome=usuario_vet.nome,
            email=usuario_vet.email,
            senha=usuario_vet.senha,
            telefone=usuario_vet.telefone,
            crmv="CRMV12345",
            verificado=True,
            bio="bioteste"
        )
        inserir_veterinario(veterinario_teste)
    
        categoria_artigo_teste = CategoriaArtigo(0, "Categoria Teste", "Descrição da categoria teste")
        id_categoria_artigo = inserir_categoria(categoria_artigo_teste)
        categoria_artigo_teste.id = id_categoria_artigo
        
        postagem_artigo_teste = PostagemArtigo(
            id=0,
            veterinario=veterinario_teste,  # objeto, não ID
            titulo="Título do Artigo Teste",
            conteudo="Conteúdo do artigo teste",
            categoria_artigo=categoria_artigo_teste,  # objeto, não ID
            data_publicacao="2023-10-01",
            visualizacoes=100  # inteiro, não string
        )
        id_postagem_artigo = inserir_artigo(postagem_artigo_teste)
        postagem_artigo_teste.id = id_postagem_artigo
        
        comentario_teste = Comentario(
            id=0,
            id_usuario=usuario_teste,  # objeto completo
            id_artigo=postagem_artigo_teste,  # objeto completo
            texto="Este é um comentário de teste",
            data_comentario=datetime.now().strftime("%Y-%m-%d"),
            data_moderacao=None
        )
        
        id_comentario_inserido = inserir(comentario_teste)
        
        comentario_db = obter_por_id(id_comentario_inserido)
        
        # ASSERTS
        assert comentario_db is not None, "O comentário inserido não deveria ser None"
        assert comentario_db.id_usuario == id_usuario, "O ID do usuário do comentário inserido não confere"
        assert comentario_db.id_artigo == id_postagem_artigo, "O ID do artigo do comentário inserido não confere"
        assert comentario_db.texto == "Este é um comentário de teste", "O texto do comentário inserido não confere"
