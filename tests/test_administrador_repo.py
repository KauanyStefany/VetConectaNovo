from repo.administrador_repo import (
    atualizar,
    atualizar_senha,
    criar_tabela,
    excluir,
    inserir,
    obter_pagina,
    obter_por_id,
)
from model.administrador_model import Administrador


class TestAdministradorRepo:
    def test_criar_tabela_administrador(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado is True, "A criação da tabela deveria retornar True"

    def test_inserir_administrador(self, test_db):
        # Arrange
        criar_tabela()
        admin_teste = Administrador(
            0, "Admin Teste", "admin@gmail.com", "12345678"
        )
        # Act
        id_admin_inserido = inserir(admin_teste)
        assert id_admin_inserido is not None
        # Assert
        admin_db = obter_por_id(id_admin_inserido)  # type: ignore[arg-type]
        assert (
            admin_db is not None
        ), "O administrador inserido não deveria ser None"
        assert (
            admin_db.id_admin == 1
        ), "O administrador inserido deveria ter um ID igual a 1"
        assert (
            admin_db.nome == "Admin Teste"
        ), "O nome do administrador inserido não confere"
        assert (
            admin_db.email == "admin@gmail.com"
        ), "O email do administrador inserido não confere"
        assert (
            admin_db.senha == "12345678"
        ), "A senha do administrador inserido não confere"

    def test_atualizar_administrador(self, test_db):
        # Arrange
        criar_tabela()
        admin_teste = Administrador(
            0, "Admin Teste", "admin@gmail.com", "12345678"
        )
        id_admin_inserido = inserir(admin_teste)
        assert id_admin_inserido is not None
        admin_inserido = obter_por_id(id_admin_inserido)  # type: ignore[arg-type]  # noqa: E501
        assert admin_inserido is not None
        # Act
        admin_inserido.nome = "Admin Atualizado"
        admin_inserido.email = "emailAtualizado@gmail.com"
        admin_inserido.senha = "12345678"
        resultado = atualizar(admin_inserido)
        # Assert
        assert (
            resultado is True
        ), "A atualização do administrador deveria retornar True"
        admin_db = obter_por_id(id_admin_inserido)  # type: ignore[arg-type]
        assert admin_db is not None
        assert (
            admin_db.nome == "Admin Atualizado"
        ), "O nome do administrador atualizado não confere"
        assert (
            admin_db.email == "emailAtualizado@gmail.com"
        ), "O email do administrador atualizado não confere"
        assert (
            admin_db.senha == "12345678"
        ), "A senha do administrador atualizado não confere"

    def test_atualizar_senha(self, test_db):
        # Arrange
        criar_tabela()
        admin_teste = Administrador(
            0, "Admin Teste", "admin@gmail.com", "12345678"
        )
        id_admin_inserido = inserir(admin_teste)
        assert id_admin_inserido is not None
        # Act
        nova_senha = "87654321"
        resultado = atualizar_senha(id_admin_inserido, nova_senha)  # type: ignore[arg-type]  # noqa: E501
        # Assert
        assert (
            resultado is True
        ), "A atualização da senha deveria retornar True"
        admin_db = obter_por_id(id_admin_inserido)  # type: ignore[arg-type]
        assert admin_db is not None
        assert (
            admin_db.senha == nova_senha
        ), "A senha do administrador atualizado não confere"

    def test_excluir_administrador(self, test_db):
        # Arrange
        criar_tabela()
        admin_teste = Administrador(
            0, "Admin Teste", "admin@gmail.com", "12345678"
        )
        id_admin_inserido = inserir(admin_teste)
        # Act
        resultado = excluir(id_admin_inserido)  # type: ignore[arg-type]
        # Assert
        assert (
            resultado is True
        ), "A exclusão do administrador deveria retornar True"
        admin_excluido = obter_por_id(id_admin_inserido)  # type: ignore[arg-type]  # noqa: E501
        assert (
            admin_excluido is None
        ), "O administrador excluído deveria ser None"

    def test_obter_todos_administradores(self, test_db):
        # Arrange
        criar_tabela()
        admin1 = Administrador(0, "Admin 1", "admin@gmail.com", "12345678")
        admin2 = Administrador(0, "Admin 2", "admin@@gmail.com", "87654321")
        inserir(admin1)
        inserir(admin2)
        # Act
        administradores = obter_pagina(0, 10)

        # Assert
        assert len(administradores) == 2, "Deveria haver 2 administradores"
        assert (
            administradores[0].nome == "Admin 1"
        ), "O nome do primeiro administrador não confere"
        assert (
            administradores[1].nome == "Admin 2"
        ), "O nome do segundo administrador não confere"

    def test_obter_administrador_por_id(self, test_db):
        # Arrange
        criar_tabela()
        admin_teste = Administrador(
            0, "Admin Teste", "admin@gmail.com", "12345678"
        )
        id_admin_inserido = inserir(admin_teste)
        # Act
        admin_obtido = obter_por_id(id_admin_inserido)  # type: ignore[arg-type]  # noqa: E501
        # Assert
        assert (
            admin_obtido is not None
        ), "O administrador obtido não deveria ser None"
        assert (
            admin_obtido.id_admin == id_admin_inserido
        ), "O ID do administrador obtido não confere"
        assert (
            admin_obtido.nome == admin_teste.nome
        ), "O nome do administrador obtido não confere"
        assert (
            admin_obtido.email == admin_teste.email
        ), "O email do administrador obtido não confere"
        assert (
            admin_obtido.senha == admin_teste.senha
        ), "A senha do administrador obtido não confere"
