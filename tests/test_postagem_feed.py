import os
import sys
from data.postagem_feed_repo import *
from data.postagem_feed_model import PostagemFeed
from data.usuario_model import Usuario
import data.usuario_repo as usuario_repo
import data.tutor_repo as tutor_repo
import data.postagem_feed_repo as postagem_repo
from data.usuario_model import Usuario
from data.tutor_model import Tutor
from data.postagem_feed_model import PostagemFeed

class TestPostagemFeedRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_postagem_feed(self, test_db):

        
        # 1. Criar tabelas na ordem correta
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_repo.criar_tabela()
        
        # 2. Inserir usuário
        usuario = Usuario(
            id_usuario=0,
            nome="Usuario Teste",
            email="usuario@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        id_usuario = usuario_repo.inserir_usuario(usuario)
        assert id_usuario is not None, "Falha ao inserir usuário"
        
        # 3. Inserir tutor
        tutor = Tutor(
            id_usuario=id_usuario,
            nome="Tutor Teste",
            email="tutor@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        id_tutor = tutor_repo.inserir_tutor(tutor)
        assert id_tutor is not None, "Falha ao inserir tutor"
        
        # 4. ✅ CORREÇÃO: Criar objeto Tutor com parâmetros corretos
        tutor_obj = Tutor(
            id_usuario=id_tutor,  # ✅ Use 'id_usuario' ao invés de 'id'
            nome="Tutor Teste",
            email="tutor@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        
        # 5. Criar postagem
        postagem_feed_teste = PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_obj,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem de teste",
            data_postagem=""
        )
        
        # Act
        id_postagem_inserido = postagem_repo.inserir(postagem_feed_teste)
        
        # Assert
        assert id_postagem_inserido is not None, "A inserção deveria retornar um ID válido"
        
        postagem_db = postagem_repo.obter_por_id(id_postagem_inserido)
        assert postagem_db is not None, "A postagem inserida não deveria ser None"
        assert postagem_db.id_postagem_feed == id_postagem_inserido
        assert postagem_db.imagem == "imagem_teste.jpg"
        assert postagem_db.descricao == "Descrição da postagem de teste"
        

        assert postagem_db.tutor.id_usuario == id_tutor, "O ID do tutor não confere"  # Use 'id_usuario'
        # OU se o modelo Tutor tem uma propriedade 'id':
        # assert postagem_db.tutor.id == id_tutor, "O ID do tutor não confere"
        
        assert postagem_db.tutor.nome == "Tutor Teste", "O nome do tutor não confere"
        assert postagem_db.data_postagem is not None