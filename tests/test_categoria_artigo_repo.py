import os
import sys
from data.categoria_artigo_repo import *
from data.categoria_artigo_model import CategoriaArtigo

class TestCategoriaArtigoRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        # Act
        resultado = criar_tabela_categoria_artigo()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_categoria(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria_teste = CategoriaArtigo(0,"Categoria Teste", "Descrição Teste")
        # Act
        id_categoria_inserida = inserir_categoria(categoria_teste)
        # Assert
        categoria_db = obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db is not None, "A categoria inserida não deveria ser None"
        assert categoria_db.id == 1, "A categoria inserida deveria ter um ID igual a 1"
        assert categoria_db.nome == "Categoria Teste", "O nome da categoria inserida não confere"
        assert categoria_db.descricao == "Descrição Teste", "O campo de descrição não pode ser vazio"

    def test_atualizar_categoria(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria_teste = CategoriaArtigo(0, "Categoria Teste", "Descrição Teste")
        id_categoria_inserida = inserir_categoria(categoria_teste)
        categoria_inserida = obter_categoria_por_id(id_categoria_inserida)
        # Act
        categoria_inserida.nome = "Categoria Atualizada"
        categoria_inserida.descricao = "Descrição Atualizada"
        resultado = atualizar_categoria(categoria_inserida)
        # Assert
        assert resultado == True, "A atualização da categoria deveria retornar True"
        categoria_db = obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db.nome == "Categoria Atualizada", "O nome da categoria atualizada não confere"
        assert categoria_db.descricao == "Descrição Atualizada", "A descrição da categoria atualizada não confere"


    def test_excluir_categoria(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria_teste = CategoriaArtigo(0, "Categoria Teste", "Descrição Teste")
        id_categoria_inserida = inserir_categoria(categoria_teste)
        # Act
        resultado = excluir_categoria(id_categoria_inserida)
        # Assert
        assert resultado == True, "A exclusão da categoria deveria retornar True"
        categoria_excluida = obter_categoria_por_id(id_categoria_inserida)
        assert categoria_excluida == None, "A categoria excluída deveria ser None"

    def test_obter_todas_categorias(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria1 = CategoriaArtigo(0, "Categoria 1", "Descrição 1")
        categoria2 = CategoriaArtigo(1, "Categoria 2", "Descrição 2")
        inserir_categoria(categoria1)
        inserir_categoria(categoria2)
        # Act
        categorias = obter_categorias_paginado(0, 5)
        # Assert
        assert len(categorias) == 2, "Deveria retornar duas categorias"
        assert categorias[0].nome == "Categoria 1", "O nome da primeira categoria não confere"
        assert categorias[1].nome == "Categoria 2", "O nome da segunda categoria não confere"

    def test_obter_categoria_por_id(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria_teste = CategoriaArtigo(0, "Categoria Teste", "Descrição Teste")
        id_categoria_inserida = inserir_categoria(categoria_teste)
        # Act
        categoria_db = obter_categoria_por_id(id_categoria_inserida)
        # Assert
        assert categoria_db is not None, "A categoria obtida não deveria ser diferente de None"
        assert categoria_db.id == id_categoria_inserida, "O ID da categoria obtida não confere"
        assert categoria_db.nome == categoria_teste.nome, "O nome da categoria obtida não confere"
        

