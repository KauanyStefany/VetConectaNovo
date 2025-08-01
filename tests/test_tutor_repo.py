import pytest
from repo.tutor_repo import *
from repo.usuario_repo import *
from model.tutor_model import Tutor
from model.usuario_model import Usuario


class TestTutorRepo:
    """Testes para o repositório de tutores"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """Setup executado antes de cada teste"""
        criar_tabela_usuario()
        criar_tabela_tutor()
        
    def test_criar_tabela(self, test_db):
        """Testa a criação da tabela de tutores"""
        # Arrange - já feito no setup
        # Act
        resultado = criar_tabela_tutor()
        
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_tutor_sucesso(self, test_db):
        """Testa inserção de tutor com sucesso"""
        # Arrange
        tutor = Tutor(
            id_usuario=0,
            nome="Maria Silva",
            email="maria.silva@email.com",
            senha="senha123",
            telefone="11987654321",
            quantidade_pets=2,
            descricao_pets="Um cachorro e um gato"
        )
        
        # Act
        id_inserido = inserir_tutor(tutor)
        
        # Assert
        assert id_inserido is not None, "ID do tutor inserido não deveria ser None"
        assert id_inserido > 0, "ID deveria ser maior que zero"
        
        # Verificar se foi salvo corretamente
        tutor_db = obter_por_id(id_inserido)
        assert tutor_db is not None, "Tutor deveria existir no banco"
        assert tutor_db.nome == tutor.nome
        assert tutor_db.email == tutor.email
        assert tutor_db.telefone == tutor.telefone
        assert tutor_db.quantidade_pets == 2
        assert tutor_db.descricao_pets == "Um cachorro e um gato"

    def test_inserir_tutor_sem_pets(self, test_db):
        """Testa inserção de tutor sem pets"""
        # Arrange
        tutor = Tutor(
            id_usuario=0,
            nome="João Santos",
            email="joao.santos@email.com",
            senha="senha456",
            telefone="11999998888",
            quantidade_pets=0,
            descricao_pets=None
        )
        
        # Act
        id_inserido = inserir_tutor(tutor)
        
        # Assert
        assert id_inserido is not None
        
        tutor_db = obter_por_id(id_inserido)
        assert tutor_db.quantidade_pets == 0
        assert tutor_db.descricao_pets is None

    def test_atualizar_tutor_sucesso(self, test_db):
        """Testa atualização de tutor com sucesso"""
        # Arrange
        tutor_original = Tutor(
            id_usuario=0,
            nome="Nome Original",
            email="original@email.com",
            senha="senha123",
            telefone="11999998888",
            quantidade_pets=1,
            descricao_pets="Um gato"
        )
        id_tutor = inserir_tutor(tutor_original)
        
        # Act
        tutor_atualizado = Tutor(
            id_usuario=id_tutor,
            nome="Nome Atualizado",
            email="atualizado@email.com",
            senha="senha123",
            telefone="11777776666",
            quantidade_pets=3,
            descricao_pets="Um gato e dois cachorros"
        )
        resultado = atualizar_tutor(tutor_atualizado)
        
        # Assert
        assert resultado == True, "Atualização deveria retornar True"
        
        tutor_db = obter_por_id(id_tutor)
        assert tutor_db.nome == "Nome Atualizado"
        assert tutor_db.email == "atualizado@email.com"
        assert tutor_db.telefone == "11777776666"
        assert tutor_db.quantidade_pets == 3
        assert tutor_db.descricao_pets == "Um gato e dois cachorros"

    def test_atualizar_tutor_inexistente(self, test_db):
        """Testa atualização de tutor inexistente"""
        # Arrange
        tutor_inexistente = Tutor(
            id_usuario=9999,
            nome="Não Existe",
            email="nao@existe.com",
            senha="senha",
            telefone="11999998888",
            quantidade_pets=0,
            descricao_pets=None
        )
        
        # Act
        resultado = atualizar_tutor(tutor_inexistente)
        
        # Assert
        assert resultado == False, "Atualização de tutor inexistente deveria retornar False"

    def test_excluir_tutor_sucesso(self, test_db):
        """Testa exclusão de tutor com sucesso"""
        # Arrange
        tutor = Tutor(
            id_usuario=0,
            nome="Para Excluir",
            email="excluir@email.com",
            senha="senha123",
            telefone="11999998888",
            quantidade_pets=1,
            descricao_pets="Um hamster"
        )
        id_tutor = inserir_tutor(tutor)
        
        # Act
        resultado = excluir_tutor(id_tutor)
        
        # Assert
        assert resultado == True, "Exclusão deveria retornar True"
        
        # Verificar se foi excluído
        tutor_db = obter_por_id(id_tutor)
        assert tutor_db is None, "Tutor não deveria mais existir"
        
        # Verificar se usuário também foi excluído
        usuario_db = obter_usuario_por_id(id_tutor)
        assert usuario_db is None, "Usuário também deveria ter sido excluído"

    def test_excluir_tutor_inexistente(self, test_db):
        """Testa exclusão de tutor inexistente"""
        # Arrange
        id_inexistente = 9999
        
        # Act
        resultado = excluir_tutor(id_inexistente)
        
        # Assert
        assert resultado == False, "Exclusão de tutor inexistente deveria retornar False"

    def test_obter_tutores_por_pagina(self, test_db):
        """Testa obtenção paginada de tutores"""
        # Arrange
        tutores = [
            Tutor(0, "Ana Costa", "ana@email.com", "senha1", "11111111111", 1, "Um gato"),
            Tutor(0, "Bruno Lima", "bruno@email.com", "senha2", "22222222222", 2, "Dois cães"),
            Tutor(0, "Carlos Silva", "carlos@email.com", "senha3", "33333333333", 0, None),
            Tutor(0, "Diana Santos", "diana@email.com", "senha4", "44444444444", 3, "Três pássaros"),
            Tutor(0, "Eduardo Souza", "eduardo@email.com", "senha5", "55555555555", 1, "Um peixe")
        ]
        
        for tutor in tutores:
            inserir_tutor(tutor)
        
        # Act - primeira página
        pagina1 = obter_tutores_por_pagina(limite=3, offset=0)
        
        # Assert
        assert len(pagina1) == 3, "Primeira página deveria ter 3 tutores"
        assert pagina1[0].nome == "Ana Costa"
        assert pagina1[1].nome == "Bruno Lima"
        assert pagina1[2].nome == "Carlos Silva"
        
        # Act - segunda página
        pagina2 = obter_tutores_por_pagina(limite=3, offset=3)
        
        # Assert
        assert len(pagina2) == 2, "Segunda página deveria ter 2 tutores"
        assert pagina2[0].nome == "Diana Santos"
        assert pagina2[1].nome == "Eduardo Souza"

    def test_obter_tutores_por_pagina_vazio(self, test_db):
        """Testa obtenção paginada quando não há tutores"""
        # Arrange - banco vazio
        # Act
        tutores = obter_tutores_por_pagina(limite=10, offset=0)
        
        # Assert
        assert len(tutores) == 0, "Lista deveria estar vazia"

    def test_obter_por_id_existente(self, test_db):
        """Testa obtenção de tutor por ID existente"""
        # Arrange
        tutor = Tutor(
            id_usuario=0,
            nome="João Silva",
            email="joao@email.com",
            senha="senha123",
            telefone="11999998888",
            quantidade_pets=4,
            descricao_pets="Dois gatos e dois cachorros"
        )
        id_tutor = inserir_tutor(tutor)
        
        # Act
        tutor_db = obter_por_id(id_tutor)
        
        # Assert
        assert tutor_db is not None, "Tutor deveria existir"
        assert tutor_db.id_usuario == id_tutor
        assert tutor_db.nome == tutor.nome
        assert tutor_db.email == tutor.email
        assert tutor_db.telefone == tutor.telefone
        assert tutor_db.quantidade_pets == 4
        assert tutor_db.descricao_pets == "Dois gatos e dois cachorros"

    def test_obter_por_id_inexistente(self, test_db):
        """Testa obtenção de tutor por ID inexistente"""
        # Arrange
        id_inexistente = 9999
        
        # Act
        tutor = obter_por_id(id_inexistente)
        
        # Assert
        assert tutor is None, "Tutor não deveria existir"

    def test_heranca_usuario(self, test_db):
        """Testa se tutor herda corretamente de usuario"""
        # Arrange
        tutor = Tutor(
            id_usuario=0,
            nome="Teste Herança",
            email="heranca@email.com",
            senha="senha123",
            telefone="11999998888",
            quantidade_pets=1,
            descricao_pets="Um coelho"
        )
        
        # Act
        id_tutor = inserir_tutor(tutor)
        
        # Assert - verificar se foi criado também como usuário
        usuario_db = obter_usuario_por_id(id_tutor)
        assert usuario_db is not None, "Deveria existir como usuário"
        assert usuario_db.nome == tutor.nome
        assert usuario_db.email == tutor.email
        
        tutor_db = obter_por_id(id_tutor)
        assert tutor_db is not None, "Deveria existir como tutor"
        assert isinstance(tutor_db, Tutor), "Deveria ser uma instância de Tutor"