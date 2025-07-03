import os
import sys
from data.postagem_feed_repo import *
from data.postagem_feed_model import PostagemFeed
from data.usuario_model import Usuario
from data import usuario_repo, usuario_sql
from data import tutor_repo
from data import postagem_feed_repo
from data.tutor_model import Tutor


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
        tutor_repo.criar_tabela_tutor()  # Assumindo que existe
        postagem_feed_repo.criar_tabela()
        
        # 2. Criar usuário primeiro
        usuario = Usuario(
            id_usuario=0,
            nome="Tutor Teste",
            email="tutor@teste.com",
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
        id_tutor = tutor_repo.inserir_tutor(tutor)  # Use a função correta do tutor_repo
        assert id_tutor is not None, "Falha ao inserir tutor"
        
        # 4. Criar objeto Tutor para a postagem
        tutor_obj = Tutor(
            id=id_tutor,  # Note: use 'id' se for assim no modelo Tutor
            nome="Tutor Teste"
        )
        
        # 5. Criar postagem
        postagem_feed_teste = PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_obj,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem de teste",
            data_postagem=""  # Será definida pelo banco
        )
        
        # Act
        id_postagem_inserido = postagem_feed_repo.inserir(postagem_feed_teste)
        
        # Assert
        assert id_postagem_inserido is not None, "A inserção deveria retornar um ID válido"
        
        postagem_db = postagem_feed_repo.obter_por_id(id_postagem_inserido)
        assert postagem_db is not None, "A postagem inserida não deveria ser None"
        assert postagem_db.id_postagem_feed == id_postagem_inserido
        assert postagem_db.imagem == "imagem_teste.jpg"
        assert postagem_db.descricao == "Descrição da postagem de teste"
        assert postagem_db.tutor.id == id_tutor
        assert postagem_db.data_postagem is not None

        