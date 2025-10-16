from datetime import datetime
import os
import sys
from repo import usuario_repo ,tutor_repo, postagem_feed_repo
from model.postagem_feed_model import PostagemFeed
from model.usuario_model import Usuario
from model.tutor_model import Tutor


class TestPostagemFeedRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = postagem_feed_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_postagem_feed(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        
        tutor = Tutor(
            id_usuario=0,
            nome="Maria",
            email="maria@email.com",
            senha="123",
            telefone="999999999",
            perfil="tutor",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            quantidade_pets=0,
            descricao_pets=None)
        id_tutor = tutor_repo.inserir_tutor(tutor)

        postagem = PostagemFeed(
            id_postagem_feed=0,
            id_tutor=id_tutor,
            imagem="imagem.jpg",
            descricao="Descrição da postagem",
            data_postagem=datetime.today().date())
        # Act
        id_post = postagem_feed_repo.inserir(postagem)
        # Assert
        assert id_post is not None, "A inserção deveria retornar um ID válido"
        postagem_db = postagem_feed_repo.obter_por_id(id_post)
        assert postagem_db is not None, "A postagem deveria ser inserida e recuperada"
        assert postagem_db.id_tutor == postagem.id_tutor, "O tutor da postagem recuperada está incorreto"
        assert postagem_db.imagem == postagem.imagem, "A imagem da postagem recuperada está incorreta"
        assert postagem_db.descricao == postagem.descricao, "A descrição da postagem recuperada está incorreta"
        assert postagem_db.data_postagem is not None, "A data da postagem não deveria ser None"

    def test_atualizar_postagem_feed_sucesso(self, test_db):
        """Testa atualização de postagem do feed com sucesso"""
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()

        tutor = Tutor(0, "Carlos", "carlos@email.com", "123", "999999999", "tutor", None, None, None, None, 1, "Cachorro")
        id_tutor = tutor_repo.inserir_tutor(tutor)

        postagem = PostagemFeed(0, id_tutor, "foto.jpg", "Descrição original", datetime.today().date())
        id_postagem = postagem_feed_repo.inserir(postagem)

        # Act
        postagem.id_postagem_feed = id_postagem
        postagem.descricao = "Descrição atualizada"
        resultado = postagem_feed_repo.atualizar(postagem)

        # Assert
        assert resultado == True, "Atualização deveria retornar True"
        postagem_db = postagem_feed_repo.obter_por_id(id_postagem)
        assert postagem_db.descricao == "Descrição atualizada", "Descrição deveria estar atualizada"

    def test_atualizar_postagem_feed_inexistente(self, test_db):
        """Testa atualização de postagem inexistente"""
        # Arrange
        postagem_feed_repo.criar_tabela()
        postagem = PostagemFeed(9999, 1, "foto.jpg", "Descrição", datetime.today().date())

        # Act
        resultado = postagem_feed_repo.atualizar(postagem)

        # Assert
        assert resultado == False, "Atualização de postagem inexistente deveria retornar False"

    def test_excluir_postagem_feed_sucesso(self, test_db):
        """Testa exclusão de postagem com sucesso"""
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()

        tutor = Tutor(0, "Ana", "ana@email.com", "123", "888888888", "tutor", None, None, None, None, 2, "Gatos")
        id_tutor = tutor_repo.inserir_tutor(tutor)

        postagem = PostagemFeed(0, id_tutor, "gato.jpg", "Meus gatos", datetime.today().date())
        id_postagem = postagem_feed_repo.inserir(postagem)

        # Act
        resultado = postagem_feed_repo.excluir(id_postagem)

        # Assert
        assert resultado == True, "Exclusão deveria retornar True"
        postagem_db = postagem_feed_repo.obter_por_id(id_postagem)
        assert postagem_db is None, "Postagem não deveria mais existir"

    def test_excluir_postagem_feed_inexistente(self, test_db):
        """Testa exclusão de postagem inexistente"""
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()

        # Act
        resultado = postagem_feed_repo.excluir(9999)

        # Assert
        assert resultado == False, "Exclusão de postagem inexistente deveria retornar False"

    def test_obter_todos_paginado(self, test_db):
        """Testa obtenção paginada de postagens"""
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()

        tutor = Tutor(0, "Pedro", "pedro@email.com", "123", "777777777", "tutor", None, None, None, None, 3, "Pets")
        id_tutor = tutor_repo.inserir_tutor(tutor)

        # Criar 5 postagens
        for i in range(5):
            postagem = PostagemFeed(0, id_tutor, f"foto{i}.jpg", f"Postagem {i}", datetime.today().date())
            postagem_feed_repo.inserir(postagem)

        # Act - primeira página (2 itens)
        pagina1 = postagem_feed_repo.obter_todos_paginado(pagina=1, tamanho_pagina=2)

        # Assert
        assert len(pagina1) == 2, "Primeira página deveria ter 2 postagens"
        assert all(isinstance(p, PostagemFeed) for p in pagina1), "Todos os itens deveriam ser PostagemFeed"

        # Act - segunda página (2 itens)
        pagina2 = postagem_feed_repo.obter_todos_paginado(pagina=2, tamanho_pagina=2)

        # Assert
        assert len(pagina2) == 2, "Segunda página deveria ter 2 postagens"

    def test_obter_todos_paginado_vazio(self, test_db):
        """Testa obtenção paginada quando não há postagens"""
        # Arrange
        postagem_feed_repo.criar_tabela()

        # Act
        postagens = postagem_feed_repo.obter_todos_paginado(pagina=1, tamanho_pagina=10)

        # Assert
        assert len(postagens) == 0, "Deveria retornar lista vazia"

    def test_obter_por_id_inexistente(self, test_db):
        """Testa obtenção de postagem inexistente"""
        # Arrange
        postagem_feed_repo.criar_tabela()

        # Act
        postagem = postagem_feed_repo.obter_por_id(9999)

        # Assert
        assert postagem is None, "Postagem inexistente deveria retornar None"
    