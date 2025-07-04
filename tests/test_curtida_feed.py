import os
import sys
from data import usuario_repo
from data import usuario_model
from data import tutor_repo
from data import tutor_model
from data import postagem_feed_repo
from data import postagem_feed_model
from data import curtida_feed_model
from data import curtida_feed_repo

class TestCurtidaFeedRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = curtida_feed_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela de curtidas do feed deveria retornar True"
        
    def test_inserir_curtida(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()
        
        # Insere um usuário
        usuario = usuario_model.Usuario(
            id_usuario=0, nome="Usuario Teste", email="usuario@gmail.com", 
            senha="senha123", telefone="12345678900"
        )
        usuario_id = usuario_repo.inserir_usuario(usuario)
        
        # Insere um tutor
        tutor = tutor_model.Tutor(
            id_usuario=usuario_id, nome="Tutor Teste", email="tutor@gmail.com", 
            senha="senha123", telefone="12345678900", cpf="12345678901", 
            endereco="Endereço Teste", verificado=False, bio=""
        )
        tutor_repo.inserir_tutor(tutor)
        
        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_model.Tutor(id_usuario=usuario_id, nome="Tutor Teste", email="tutor@gmail.com", 
                       senha="senha123", telefone="12345678900", cpf="12345678901", 
                       endereco="Endereço Teste", verificado=False, bio=""),
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=""
        )
        postagem_id = postagem_feed_repo.inserir(postagem)
        
        # Cria uma curtida
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=usuario_id,
            id_postagem_feed=postagem_id
        )
        
        # Act
        resultado = curtida_feed_repo.inserir(curtida)
        
        # Assert
        assert resultado == True, "A inserção da curtida deveria retornar True"
        curtida_db = curtida_feed_repo.obter_por_id(usuario_id, postagem_id)
        assert curtida_db is not None, "A curtida inserida não deveria ser None"
        assert curtida_db.id_usuario == usuario_id, "O ID do usuário da curtida inserida não confere"
        assert curtida_db.id_postagem_feed == postagem_id, "O ID da postagem da curtida inserida não confere"
        assert curtida_db.data_curtida is not None, "A data da curtida inserida não deveria ser None"

    def test_excluir_curtida(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()
        
        # Insere um usuário
        usuario = usuario_model.Usuario(
            id_usuario=0, nome="Usuario Teste", email="usuario@gmail.com", 
            senha="senha123", telefone="12345678900"
        )
        usuario_id = usuario_repo.inserir_usuario(usuario)
        
        # Insere um tutor
        tutor = tutor_model.Tutor(
            id_usuario=usuario_id, nome="Tutor Teste", email="tutor@gmail.com", 
            senha="senha123", telefone="12345678900", cpf="12345678901", 
            endereco="Endereço Teste", verificado=False, bio=""
        )
        tutor_repo.inserir_tutor(tutor)
        
        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_model.Tutor(id_usuario=usuario_id, nome="Tutor Teste", email="tutor@gmail.com", 
                       senha="senha123", telefone="12345678900", cpf="12345678901", 
                       endereco="Endereço Teste", verificado=False, bio=""),
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=""
        )
        postagem_id = postagem_feed_repo.inserir(postagem)
        
        # Insere uma curtida
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=usuario_id,
            id_postagem_feed=postagem_id
        )
        curtida_feed_repo.inserir(curtida)
        
        # Act
        resultado = curtida_feed_repo.excluir(usuario_id, postagem_id)
        
        # Assert
        assert resultado == True, "A exclusão da curtida deveria retornar True"
        curtida_db = curtida_feed_repo.obter_por_id(usuario_id, postagem_id)
        assert curtida_db is None, "A curtida excluída deveria ser None após exclusão"
    
    def test_obter_todas_paginado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()
        
        # Insere um usuário
        usuario = usuario_model.Usuario(
            id_usuario=0, nome="Usuario Teste", email="usuario@gmail.com", 
            senha="senha123", telefone="12345678900"
        )
        usuario_id = usuario_repo.inserir_usuario(usuario)
        
        # Insere um tutor
        tutor = tutor_model.Tutor(
            id_usuario=usuario_id, nome="Tutor Teste", email="tutor@gmail.com", 
            senha="senha123", telefone="12345678900", cpf="12345678901", 
            endereco="Endereço Teste", verificado=False, bio=""
        )
        tutor_repo.inserir_tutor(tutor)
        
        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_model.Tutor(id_usuario=usuario_id, nome="Tutor Teste", email="tutor@gmail.com", 
                       senha="senha123", telefone="12345678900", cpf="12345678901", 
                       endereco="Endereço Teste", verificado=False, bio=""),
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=""
        )
        postagem_id = postagem_feed_repo.inserir(postagem)
        
        # Insere uma curtida
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=usuario_id,
            id_postagem_feed=postagem_id
        )
        curtida_feed_repo.inserir(curtida)
        
        # Act
        resultado = curtida_feed_repo.obter_todos_paginado(10, 0)
        
        # Assert
        
        assert resultado is not None, "A consulta de curtidas deveria retornar resultados"
        assert len(resultado) > 0, "A consulta de curtidas deveria retornar mais de 0 resultados"
        assert resultado[0].id_usuario == usuario_id, "O ID do usuário na curtida retornada não confere"
        assert resultado[0].id_postagem_feed == postagem_id, "O ID da postagem na curtida retornada não confere"
        assert resultado[0].data_curtida is not None, "A data da curtida retornada não deveria ser None"
        
    def test_obter_por_id(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()
        
        # Insere um usuário
        usuario = usuario_model.Usuario(
            id_usuario=0, nome="Usuario Teste", email="usuario@gmail.com", 
            senha="senha123", telefone="12345678900"
        )
        usuario_id = usuario_repo.inserir_usuario(usuario)
        
        # Insere um tutor
        tutor = tutor_model.Tutor(
            id_usuario=usuario_id, nome="Tutor Teste", email="tutor@gmail.com", 
            senha="senha123", telefone="12345678900", cpf="12345678901", 
            endereco="Endereço Teste", verificado=False, bio=""
        )
        tutor_repo.inserir_tutor(tutor)
        
        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_model.Tutor(id_usuario=usuario_id, nome="Tutor Teste", email="tutor@gmail.com", 
                       senha="senha123", telefone="12345678900", cpf="12345678901", 
                       endereco="Endereço Teste", verificado=False, bio=""),
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=""
        )
        postagem_id = postagem_feed_repo.inserir(postagem)
        
        # Insere uma curtida
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=usuario_id,
            id_postagem_feed=postagem_id
            
        )
        curtida_feed_repo.inserir(curtida)
        
        # Act
        resultado = curtida_feed_repo.obter_por_id(usuario_id, postagem_id)
        
        # Assert
        assert resultado is not None, "A consulta de curtida deveria retornar um resultado"
        assert resultado.id_usuario == usuario_id, "O ID do usuário na curtida retornada não confere"
        assert resultado.id_postagem_feed == postagem_id, "O ID da postagem na curtida retornada não confere"
        assert resultado.data_curtida is not None, "A data da curtida retornada não deveria ser None"