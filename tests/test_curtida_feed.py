import os
import sys
import time
from datetime import date
from app.database.repositories import usuario_repo
from app.database.models import usuario_model
from app.database.repositories import tutor_repo
from app.database.models import tutor_model
from app.database.repositories import postagem_feed_repo
from app.database.models import postagem_feed_model
from app.database.models import curtida_feed_model
from app.database.repositories import curtida_feed_repo

def unique_email(prefix="test"):
    """Gera um email único para testes"""
    timestamp = str(int(time.time() * 1000000))
    return f"{prefix}_{timestamp}@test.com"

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
        
        # Insere um tutor (que também cria o usuário)
        tutor = tutor_model.Tutor(
            id_usuario=0, nome="Tutor Teste", email=unique_email("tutor"),
            senha="senha123", telefone="12345678901", quantidade_pets=2,
            descricao_pets="Dois gatos"
        )
        tutor_id = tutor_repo.inserir_tutor(tutor)
        
        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            id_tutor=tutor_id,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=date.today()
        )
        postagem_id = postagem_feed_repo.inserir(postagem)
        
        # Cria uma curtida
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=tutor_id,
            id_postagem_feed=postagem_id
        )
        
        # Act
        resultado = curtida_feed_repo.inserir(curtida)
        
        # Assert
        assert resultado == True, "A inserção da curtida deveria retornar True"
        curtida_db = curtida_feed_repo.obter_por_id(tutor_id, postagem_id)
        assert curtida_db is not None, "A curtida inserida não deveria ser None"
        assert curtida_db.id_usuario == tutor_id, "O ID do usuário da curtida inserida não confere"
        assert curtida_db.id_postagem_feed == postagem_id, "O ID da postagem da curtida inserida não confere"
        assert curtida_db.data_curtida is not None, "A data da curtida inserida não deveria ser None"

    def test_excluir_curtida(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()
        
        # Insere um tutor (que também cria o usuário)
        tutor = tutor_model.Tutor(
            id_usuario=0, nome="Tutor Teste", email=unique_email("tutor2"),
            senha="senha123", telefone="12345678911", quantidade_pets=2,
            descricao_pets="Dois gatos"
        )
        tutor_id = tutor_repo.inserir_tutor(tutor)
        
        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            id_tutor=tutor_id,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=date.today()
        )
        postagem_id = postagem_feed_repo.inserir(postagem)
        
        # Insere uma curtida
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=tutor_id,
            id_postagem_feed=postagem_id
        )
        curtida_feed_repo.inserir(curtida)
        
        # Act
        resultado = curtida_feed_repo.excluir(tutor_id, postagem_id)
        
        # Assert
        assert resultado == True, "A exclusão da curtida deveria retornar True"
        curtida_db = curtida_feed_repo.obter_por_id(tutor_id, postagem_id)
        assert curtida_db is None, "A curtida excluída deveria ser None após exclusão"
    
    def test_obter_todas_paginado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()
        
        # Insere um tutor (que também cria o usuário)
        tutor = tutor_model.Tutor(
            id_usuario=0, nome="Tutor Teste", email=unique_email("tutor3"),
            senha="senha123", telefone="12345678921", quantidade_pets=2,
            descricao_pets="Dois gatos"
        )
        tutor_id = tutor_repo.inserir_tutor(tutor)
        
        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            id_tutor=tutor_id,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=date.today()
        )
        postagem_id = postagem_feed_repo.inserir(postagem)
        
        # Insere uma curtida
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=tutor_id,
            id_postagem_feed=postagem_id
        )
        curtida_feed_repo.inserir(curtida)
        
        # Act
        resultado = curtida_feed_repo.obter_todos_paginado(10, 0)
        
        # Assert
        assert resultado is not None, "A consulta de curtidas deveria retornar resultados"
        assert len(resultado) > 0, "A consulta de curtidas deveria retornar mais de 0 resultados"

        # Verificar se nossa curtida está na lista
        nossa_curtida = None
        for curtida in resultado:
            if curtida.id_usuario == tutor_id and curtida.id_postagem_feed == postagem_id:
                nossa_curtida = curtida
                break

        assert nossa_curtida is not None, "Nossa curtida deveria estar na lista retornada"
        assert nossa_curtida.data_curtida is not None, "A data da curtida retornada não deveria ser None"
        
    def test_obter_por_id(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()
        
        # Insere um tutor (que também cria o usuário)
        tutor = tutor_model.Tutor(
            id_usuario=0, nome="Tutor Teste", email=unique_email("tutor4"),
            senha="senha123", telefone="12345678931", quantidade_pets=2,
            descricao_pets="Dois gatos"
        )
        tutor_id = tutor_repo.inserir_tutor(tutor)
        
        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            id_tutor=tutor_id,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=date.today()
        )
        postagem_id = postagem_feed_repo.inserir(postagem)
        
        # Insere uma curtida
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=tutor_id,
            id_postagem_feed=postagem_id
        )
        curtida_feed_repo.inserir(curtida)
        
        # Act
        resultado = curtida_feed_repo.obter_por_id(tutor_id, postagem_id)
        
        # Assert
        assert resultado is not None, "A consulta de curtida deveria retornar um resultado"
        assert resultado.id_usuario == tutor_id, "O ID do usuário na curtida retornada não confere"
        assert resultado.id_postagem_feed == postagem_id, "O ID da postagem na curtida retornada não confere"
        assert resultado.data_curtida is not None, "A data da curtida retornada não deveria ser None"