# import os  # noqa: F401
# import sys  # noqa: F401
from datetime import date
from repo import usuario_repo
# from model import usuario_model  # noqa: F401
from repo import tutor_repo
from model import tutor_model
from repo import postagem_feed_repo
from model import postagem_feed_model
from model import curtida_feed_model
from repo import curtida_feed_repo


class TestCurtidaFeedRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = curtida_feed_repo.criar_tabela()
        # Assert
        assert (
            resultado is True
        ), "A criação da tabela de curtidas do feed deveria retornar True"

    def test_inserir_curtida(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        tutor_repo.criar_tabela()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()

        # Insere um tutor (que também cria o usuário)
        tutor = tutor_model.Tutor(
            id_usuario=0,
            nome="Tutor Teste",
            email="tutor_teste@gmail.com",
            senha="senha123",
            telefone="12345678901",
            perfil="tutor",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            quantidade_pets=2,
            descricao_pets="Dois gatos",
        )
        tutor_id = tutor_repo.inserir(tutor)
        assert tutor_id is not None

        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            id_tutor=tutor_id,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=date.today(),
        )
        postagem_id = postagem_feed_repo.inserir(postagem)
        assert postagem_id is not None

        # Cria uma curtida
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=tutor_id, id_postagem_feed=postagem_id
        )

        # Act
        resultado = curtida_feed_repo.inserir(curtida)

        # Assert
        assert resultado is True, "A inserção da curtida deveria retornar True"
        curtida_db = curtida_feed_repo.obter_por_id(tutor_id, postagem_id)
        assert curtida_db is not None
        assert (
            curtida_db is not None
        ), "A curtida inserida não deveria ser None"
        assert (
            curtida_db.id_usuario == tutor_id
        ), "O ID do usuário da curtida inserida não confere"
        assert (
            curtida_db.id_postagem_feed == postagem_id
        ), "O ID da postagem da curtida inserida não confere"
        assert (
            curtida_db.data_curtida is not None
        ), "A data da curtida inserida não deveria ser None"

    def test_excluir_curtida(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        tutor_repo.criar_tabela()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()

        # Insere um tutor (que também cria o usuário)
        tutor = tutor_model.Tutor(
            id_usuario=0,
            nome="Tutor Teste",
            email="tutor_teste2@gmail.com",
            senha="senha123",
            telefone="12345678911",
            perfil="tutor",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            quantidade_pets=2,
            descricao_pets="Dois gatos",
        )
        tutor_id = tutor_repo.inserir(tutor)
        assert tutor_id is not None

        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            id_tutor=tutor_id,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=date.today(),
        )
        postagem_id = postagem_feed_repo.inserir(postagem)

        # Insere uma curtida
        assert tutor_id is not None
        assert postagem_id is not None
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=tutor_id, id_postagem_feed=postagem_id
        )
        curtida_feed_repo.inserir(curtida)

        # Act
        assert tutor_id is not None
        assert postagem_id is not None
        resultado = curtida_feed_repo.excluir(tutor_id, postagem_id)

        # Assert
        assert resultado is True, "A exclusão da curtida deveria retornar True"
        assert tutor_id is not None
        assert postagem_id is not None
        curtida_db = curtida_feed_repo.obter_por_id(tutor_id, postagem_id)
        assert (
            curtida_db is None
        ), "A curtida excluída deveria ser None após exclusão"

    def test_obter_todas_paginado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        tutor_repo.criar_tabela()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()

        # Insere um tutor (que também cria o usuário)
        tutor = tutor_model.Tutor(
            id_usuario=0,
            nome="Tutor Teste",
            email="tutor_teste3@gmail.com",
            senha="senha123",
            telefone="12345678921",
            perfil="tutor",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            quantidade_pets=2,
            descricao_pets="Dois gatos",
        )
        tutor_id = tutor_repo.inserir(tutor)
        assert tutor_id is not None

        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            id_tutor=tutor_id,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=date.today(),
        )
        postagem_id = postagem_feed_repo.inserir(postagem)

        # Insere uma curtida
        assert tutor_id is not None
        assert postagem_id is not None
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=tutor_id, id_postagem_feed=postagem_id
        )
        curtida_feed_repo.inserir(curtida)

        # Act
        resultado = curtida_feed_repo.obter_pagina(10, 0)

        # Assert
        assert (
            resultado is not None
        ), "A consulta de curtidas deveria retornar resultados"
        assert len(resultado) > 0
        assert (
            len(resultado) > 0
        ), "A consulta de curtidas deveria retornar mais de 0 resultados"
        assert (
            resultado[0].id_usuario == tutor_id
        ), "O ID do usuário na curtida retornada não confere"
        assert (
            resultado[0].id_postagem_feed == postagem_id
        ), "O ID da postagem na curtida retornada não confere"
        assert (
            resultado[0].data_curtida is not None
        ), "A data da curtida retornada não deveria ser None"

    def test_obter_por_id(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        tutor_repo.criar_tabela()
        postagem_feed_repo.criar_tabela()
        curtida_feed_repo.criar_tabela()

        # Insere um tutor (que também cria o usuário)
        tutor = tutor_model.Tutor(
            id_usuario=0,
            nome="Tutor Teste",
            email="tutor_teste4@gmail.com",
            senha="senha123",
            telefone="12345678931",
            perfil="tutor",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            quantidade_pets=2,
            descricao_pets="Dois gatos",
        )
        tutor_id = tutor_repo.inserir(tutor)
        assert tutor_id is not None

        # Insere uma postagem do feed
        postagem = postagem_feed_model.PostagemFeed(
            id_postagem_feed=0,
            id_tutor=tutor_id,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem teste",
            data_postagem=date.today(),
        )
        postagem_id = postagem_feed_repo.inserir(postagem)

        # Insere uma curtida
        assert tutor_id is not None
        assert postagem_id is not None
        curtida = curtida_feed_model.CurtidaFeed(
            id_usuario=tutor_id, id_postagem_feed=postagem_id
        )
        curtida_feed_repo.inserir(curtida)

        # Act
        assert tutor_id is not None
        assert postagem_id is not None
        resultado = curtida_feed_repo.obter_por_id(tutor_id, postagem_id)

        # Assert
        assert (
            resultado is not None
        ), "A consulta de curtida deveria retornar um resultado"
        assert (
            resultado.id_usuario == tutor_id
        ), "O ID do usuário na curtida retornada não confere"
        assert (
            resultado.id_postagem_feed == postagem_id
        ), "O ID da postagem na curtida retornada não confere"
        assert (
            resultado.data_curtida is not None
        ), "A data da curtida retornada não deveria ser None"
