from datetime import datetime
import os
import sys
from data import usuario_repo ,tutor_repo, postagem_feed_repo
from data.postagem_feed_model import PostagemFeed
from data.usuario_model import Usuario
from data.tutor_model import Tutor


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
            telefone="999999999")
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
        assert postagem_db.tutor.id_usuario == postagem.tutor.id_usuario, "O tutor da postagem recuperada está incorreto"
        assert postagem_db.imagem == postagem.imagem, "A imagem da postagem recuperada está incorreta"
        assert postagem_db.descricao == postagem.descricao, "A descrição da postagem recuperada está incorreta"
        assert postagem_db.data_postagem == postagem.data_postagem, "A data da postagem recuperada está incorreta"
    