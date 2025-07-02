import os
import sys
import pytest
from data.usuario_model import Usuario
from data.postagem_artigo_model import PostagemArtigo
from data.comentario_model import Comentario
from datetime import datetime
from data import comentario_repo, usuario_repo, postagem_artigo_repo
#from data.comentario_repo import *

class TestComentarioRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db):
        # Arrange: prepara o banco e cria a tabela
        criar_tabela()
        comentario_teste = Comentario(0, "Usuario", "Artigo", "Texto", "Data Comentario", "Data Moderação")
        # Act: insere o tutor de exemplo
        id_comentario_inserido = inserir(comentario_teste)
        # Assert: verifica se o tutor foi inserido corretamente
        comentario_db = obter_por_id(id_comentario_inserido)

        assert comentario_db is not None, "O comentário inserido não deveria ser None"
        assert comentario_db.usuario > "Usuario", "O usuário inserido deveria ter um ID válido"
        assert comentario_db.artigo == "Artigo", "O nome do artigo não confere"
        assert comentario_db.texto == "Texto", "O texto do comentario não confere"
        assert comentario_db.data_comentario == "Data Comentario", "A data do comentário não confere"
        assert comentario_db.data_moderacao == "Data Moderação", "A data da moderação não confere"


    def test_atualizar(self, test_db):
        # Arrange
        criar_tabela()
        comentario_teste = Comentario(0, "Texto Teste", "Data da Moderacao Teste")
        comentario_inserido = inserir(comentario_teste)
        # Act
        comentario_inserido.texto = "Texto Atualizado"
        comentario_inserido.data_moderacao = "Data da Moderacao Atualizado"
        resultado = atualizar(comentario_inserido)
        # Assert
        assert resultado == True, "A atualização do comentário deveria retornar True"
        comentario_db = obter_por_id(comentario_inserido)
        assert comentario_db.texto == "Texto atualizado", "O Texto do comentário atualizado não confere"
        assert comentario_db.data_moderacao == "Data da Moderacao Atualizada", "A Data da Moderacao do comentário atualizada não confere"

    


@pytest.fixture
def usuario_exemplo():
    return Usuario(0, "Usuário Teste", "teste@email.com", "senha123", "11999999999")

@pytest.fixture
def artigo_exemplo():
    return PostagemArtigo(0, "Título Teste", "Conteúdo Teste", datetime.now(), True, 1)

@pytest.fixture
def comentario_exemplo():
    return Comentario(0, None, None, "Comentário de Teste", datetime.now(), None)


# ------------------ TESTES ------------------

class TestComentarioRepo:
    def test_criar_tabela(self, test_db):
        resultado = comentario_repo.criar_tabela()
        assert resultado is True, "A criação da tabela de comentários deveria retornar True"

    def test_inserir(self, test_db, usuario_exemplo, artigo_exemplo, comentario_exemplo):
        usuario_repo.criar_tabela_usuario()
        postagem_artigo_repo.criar_tabela()
        comentario_repo.criar_tabela()

        id_usuario = usuario_repo.inserir_usuario(usuario_exemplo)
        id_artigo = postagem_artigo_repo.inserir(artigo_exemplo)

        comentario_exemplo.usuario = id_usuario
        comentario_exemplo.artigo = id_artigo

        id_comentario = comentario_repo.inserir(comentario_exemplo)
        comentario_db = comentario_repo.obter_por_id(id_comentario)

        assert comentario_db is not None
        assert comentario_db.id == id_comentario
        assert comentario_db.texto == comentario_exemplo.texto

    def test_atualizar(self, test_db, usuario_exemplo, artigo_exemplo, comentario_exemplo):
        usuario_repo.criar_tabela_usuario()
        postagem_artigo_repo.criar_tabela()
        comentario_repo.criar_tabela()

        id_usuario = usuario_repo.inserir_usuario(usuario_exemplo)
        id_artigo = postagem_artigo_repo.inserir_postagem(artigo_exemplo)

        comentario_exemplo.usuario = id_usuario
        comentario_exemplo.artigo = id_artigo
        id_comentario = comentario_repo.inserir(comentario_exemplo)

        comentario_exemplo.id = id_comentario
        comentario_exemplo.texto = "Comentário Atualizado"
        comentario_exemplo.data_moderacao = "2024-01-01"

        atualizado = comentario_repo.atualizar(comentario_exemplo)
        comentario_db = comentario_repo.obter_por_id(id_comentario)

        assert atualizado is True
        assert comentario_db.texto == "Comentário Atualizado"
        assert comentario_db.data_moderacao == "2024-01-01"

    def test_excluir(self, test_db, usuario_exemplo, artigo_exemplo, comentario_exemplo):
        usuario_repo.criar_tabela_usuarios()
        postagem_artigo_repo.criar_tabela_postagens()
        comentario_repo.criar_tabela()

        id_usuario = usuario_repo.inserir_usuario(usuario_exemplo)
        id_artigo = postagem_artigo_repo.inserir_postagem(artigo_exemplo)

        comentario_exemplo.usuario = id_usuario
        comentario_exemplo.artigo = id_artigo
        id_comentario = comentario_repo.inserir(comentario_exemplo)

        excluido = comentario_repo.excluir(id_comentario)
        comentario_db = comentario_repo.obter_por_id(id_comentario)

        assert excluido is True
        assert comentario_db is None

    def test_obter_todos_paginado(self, test_db, usuario_exemplo, artigo_exemplo, comentario_exemplo):
        usuario_repo.criar_tabela_usuarios()
        postagem_artigo_repo.criar_tabela_postagens()
        comentario_repo.criar_tabela()

        id_usuario = usuario_repo.inserir_usuario(usuario_exemplo)
        id_artigo = postagem_artigo_repo.inserir_postagem(artigo_exemplo)

        for i in range(3):
            comentario_exemplo.usuario = id_usuario
            comentario_exemplo.artigo = id_artigo
            comentario_exemplo.texto = f"Comentário {i+1}"
            comentario_repo.inserir(comentario_exemplo)

        comentarios = comentario_repo.obter_todos_paginado(limite=10, offset=0)

        assert len(comentarios) == 3
        assert comentarios[0].texto == "Comentário 1"
        assert comentarios[1].id_usuario.id_usuario == id_usuario
        assert comentarios[2].id_artigo.id == id_artigo

