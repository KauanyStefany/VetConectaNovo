import pytest
from repo.categoria_artigo_repo import *
from model.categoria_artigo_model import CategoriaArtigo


class TestCategoriaArtigoRepo:
    """Testes para o repositório de categorias de artigos"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """Setup executado antes de cada teste"""
        criar_tabela_categoria_artigo()
        
    def test_criar_tabela(self, test_db):
        """Testa a criação da tabela de categorias"""
        # Arrange - já feito no setup
        # Act
        resultado = criar_tabela_categoria_artigo()
        
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_categoria_sucesso(self, test_db):
        """Testa inserção de categoria com sucesso"""
        # Arrange
        categoria = CategoriaArtigo(
            id_categoria_artigo=0,  # 0 para auto-increment
            nome="Nutrição Animal",
            descricao="Artigos sobre alimentação e nutrição de pets"
        )
        
        # Act
        id_inserido = inserir_categoria(categoria)
        
        # Assert
        assert id_inserido is not None, "ID da categoria inserida não deveria ser None"
        assert id_inserido > 0, "ID deveria ser maior que zero"
        
        # Verificar se foi salvo corretamente
        categoria_db = obter_categoria_por_id(id_inserido)
        assert categoria_db is not None, "Categoria deveria existir no banco"
        assert categoria_db.nome == categoria.nome
        assert categoria_db.descricao == categoria.descricao

    def test_inserir_categoria_sem_descricao(self, test_db):
        """Testa inserção de categoria sem descrição"""
        # Arrange
        categoria = CategoriaArtigo(
            id_categoria_artigo=0,
            nome="Comportamento",
            descricao=None
        )
        
        # Act
        id_inserido = inserir_categoria(categoria)
        
        # Assert
        assert id_inserido is not None, "Deveria permitir inserir categoria sem descrição"
        
        categoria_db = obter_categoria_por_id(id_inserido)
        assert categoria_db.nome == "Comportamento"
        assert categoria_db.descricao is None

    def test_atualizar_categoria_sucesso(self, test_db):
        """Testa atualização de categoria com sucesso"""
        # Arrange
        categoria_original = CategoriaArtigo(0, "Nome Original", "Descrição Original")
        id_categoria = inserir_categoria(categoria_original)
        
        # Act
        categoria_atualizada = CategoriaArtigo(
            id_categoria_artigo=id_categoria,
            nome="Nome Atualizado",
            descricao="Descrição Atualizada"
        )
        resultado = atualizar_categoria(categoria_atualizada)
        
        # Assert
        assert resultado == True, "Atualização deveria retornar True"
        
        categoria_db = obter_categoria_por_id(id_categoria)
        assert categoria_db.nome == "Nome Atualizado"
        assert categoria_db.descricao == "Descrição Atualizada"

    def test_atualizar_categoria_inexistente(self, test_db):
        """Testa atualização de categoria inexistente"""
        # Arrange
        categoria_inexistente = CategoriaArtigo(9999, "Não Existe", "Descrição")
        
        # Act
        resultado = atualizar_categoria(categoria_inexistente)
        
        # Assert
        assert resultado == False, "Atualização de categoria inexistente deveria retornar False"

    def test_excluir_categoria_sucesso(self, test_db):
        """Testa exclusão de categoria com sucesso"""
        # Arrange
        categoria = CategoriaArtigo(0, "Para Excluir", "Será excluída")
        id_categoria = inserir_categoria(categoria)
        
        # Act
        resultado = excluir_categoria(id_categoria)
        
        # Assert
        assert resultado == True, "Exclusão deveria retornar True"
        
        categoria_db = obter_categoria_por_id(id_categoria)
        assert categoria_db is None, "Categoria não deveria mais existir"

    def test_excluir_categoria_inexistente(self, test_db):
        """Testa exclusão de categoria inexistente"""
        # Arrange
        id_inexistente = 9999
        
        # Act
        resultado = excluir_categoria(id_inexistente)
        
        # Assert
        assert resultado == False, "Exclusão de categoria inexistente deveria retornar False"

    def test_obter_categorias_paginado(self, test_db):
        """Testa obtenção paginada de categorias"""
        # Arrange
        categorias = [
            CategoriaArtigo(0, "Alimentação", "Tudo sobre nutrição animal"),
            CategoriaArtigo(0, "Comportamento", "Psicologia e comportamento animal"),
            CategoriaArtigo(0, "Doenças", "Patologias veterinárias"),
            CategoriaArtigo(0, "Emergências", "Primeiros socorros e emergências"),
            CategoriaArtigo(0, "Filhotes", "Cuidados com filhotes")
        ]
        
        for categoria in categorias:
            inserir_categoria(categoria)
        
        # Act - primeira página
        pagina1 = obter_categorias_paginado(offset=0, limite=3)
        
        # Assert
        assert len(pagina1) == 3, "Primeira página deveria ter 3 categorias"
        assert pagina1[0].nome == "Alimentação"
        assert pagina1[1].nome == "Comportamento"
        assert pagina1[2].nome == "Doenças"
        
        # Act - segunda página
        pagina2 = obter_categorias_paginado(offset=3, limite=3)
        
        # Assert
        assert len(pagina2) == 2, "Segunda página deveria ter 2 categorias"
        assert pagina2[0].nome == "Emergências"
        assert pagina2[1].nome == "Filhotes"

    def test_obter_categorias_paginado_vazio(self, test_db):
        """Testa obtenção paginada quando não há categorias"""
        # Arrange - banco vazio
        # Act
        categorias = obter_categorias_paginado(offset=0, limite=10)
        
        # Assert
        assert len(categorias) == 0, "Lista deveria estar vazia"

    def test_obter_categoria_por_id_existente(self, test_db):
        """Testa obtenção de categoria por ID existente"""
        # Arrange
        categoria = CategoriaArtigo(0, "Nutrição", "Artigos sobre nutrição")
        id_categoria = inserir_categoria(categoria)
        
        # Act
        categoria_db = obter_categoria_por_id(id_categoria)
        
        # Assert
        assert categoria_db is not None, "Categoria deveria existir"
        assert categoria_db.id_categoria_artigo == id_categoria
        assert categoria_db.nome == categoria.nome
        assert categoria_db.descricao == categoria.descricao

    def test_obter_categoria_por_id_inexistente(self, test_db):
        """Testa obtenção de categoria por ID inexistente"""
        # Arrange
        id_inexistente = 9999
        
        # Act
        categoria = obter_categoria_por_id(id_inexistente)
        
        # Assert
        assert categoria is None, "Categoria não deveria existir"

    def test_ordenacao_por_nome(self, test_db):
        """Testa se a ordenação por nome está funcionando"""
        # Arrange
        categorias = [
            CategoriaArtigo(0, "Zebra", None),
            CategoriaArtigo(0, "Abelha", None),
            CategoriaArtigo(0, "Macaco", None)
        ]
        
        for categoria in categorias:
            inserir_categoria(categoria)
        
        # Act
        categorias_ordenadas = obter_categorias_paginado(offset=0, limite=10)
        
        # Assert
        assert len(categorias_ordenadas) == 3
        assert categorias_ordenadas[0].nome == "Abelha"
        assert categorias_ordenadas[1].nome == "Macaco"
        assert categorias_ordenadas[2].nome == "Zebra"