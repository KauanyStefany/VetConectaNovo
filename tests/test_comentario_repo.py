import os
import sys
from data.comentario_model import Comentario
from data.comentario_repo import *


class TestComentarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela de comentários deveria retornar True"

    def test_inserir_comentario(self, test_db):
        # Arrange
        criar_tabela()
        comentario_teste = Comentario(
            id=0,
            id_usuario=1,  # Supondo que o usuário com ID 1 já exista
            id_artigo=1,   # Supondo que o artigo com ID 1 já exista
            texto="Este é um comentário de teste"
        )
        # Act
        id_comentario_inserido = inserir(comentario_teste)
        # Assert
        assert id_comentario_inserido is not None, "A inserção do comentário deveria retornar um ID válido"
        comentario_db = obter_todos_paginado(10, 0)[0]
        assert comentario_db is not None, "O comentário inserido não deveria ser None"
        assert comentario_db.texto == "Este é um comentário de teste", "O texto do comentário inserido não confere"
        
    def test_atualizar_comentario(self, test_db):
        # Arrange
        criar_tabela()
        comentario_teste = Comentario(
            id=1,
            id_usuario=1,  # Supondo que o usuário com ID 1 já exista
            id_artigo=1,   # Supondo que o artigo com ID 1 já exista
            texto="Comentário original"
        )
        inserir(comentario_teste)
        comentario_teste.texto = "Comentário atualizado"
        # Act
        resultado = atualizar(comentario_teste)
        # Assert
        assert resultado == True, "A atualização do comentário deveria retornar True"
        comentario_db = obter_todos_paginado(10, 0)[0]
        assert comentario_db.texto == "Comentário atualizado", "O texto do comentário atualizado não confere"