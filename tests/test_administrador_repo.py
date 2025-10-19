import pytest
from repo.administrador_repo import (
    atualizar,
    atualizar_senha,
    criar_tabela,
    excluir,
    inserir,
    obter_pagina,
    obter_por_id,
    importar,
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

    def test_importar_administrador_sucesso(self, test_db):
        """Testa importação de administrador com ID específico"""
        # Arrange
        criar_tabela()
        admin_importado = Administrador(
            id_admin=100,  # ID específico para importação
            nome="Admin Importado",
            email="admin.importado@gmail.com",
            senha="12345678",
        )

        # Act
        resultado = importar(admin_importado)

        # Assert
        assert resultado is True, "Importação deveria retornar True"

        # Verificar se foi salvo com o ID correto
        admin_db = obter_por_id(100)
        assert admin_db is not None, "Administrador importado deveria existir"
        assert admin_db.id_admin == 100, "ID deveria ser 100"
        assert admin_db.nome == "Admin Importado"
        assert admin_db.email == "admin.importado@gmail.com"
        assert admin_db.senha == "12345678"

    def test_importar_administrador_id_duplicado(self, test_db):
        """Testa importação de administrador com ID duplicado"""
        # Arrange
        criar_tabela()
        admin1 = Administrador(
            id_admin=200,
            nome="Admin Primeiro",
            email="primeiro@gmail.com",
            senha="12345678",
        )
        admin2 = Administrador(
            id_admin=200,  # Mesmo ID
            nome="Admin Segundo",
            email="segundo@gmail.com",
            senha="87654321",
        )

        # Act
        resultado1 = importar(admin1)
        assert resultado1 is True

        # Assert - deve falhar por ID duplicado
        with pytest.raises(Exception):
            importar(admin2)

    def test_importar_multiplos_administradores(self, test_db):
        """Testa importação de múltiplos administradores com IDs específicos"""
        # Arrange
        criar_tabela()
        administradores = [
            Administrador(
                id_admin=301,
                nome="Admin 1",
                email="admin1@gmail.com",
                senha="senha001",
            ),
            Administrador(
                id_admin=302,
                nome="Admin 2",
                email="admin2@gmail.com",
                senha="senha002",
            ),
            Administrador(
                id_admin=303,
                nome="Admin 3",
                email="admin3@gmail.com",
                senha="senha003",
            ),
        ]

        # Act
        for admin in administradores:
            resultado = importar(admin)
            assert (
                resultado is True
            ), f"Importação de {admin.nome} deveria retornar True"

        # Assert
        admin1_db = obter_por_id(301)
        admin2_db = obter_por_id(302)
        admin3_db = obter_por_id(303)

        assert admin1_db is not None and admin1_db.id_admin == 301
        assert admin2_db is not None and admin2_db.id_admin == 302
        assert admin3_db is not None and admin3_db.id_admin == 303

        assert admin1_db.nome == "Admin 1"
        assert admin2_db.nome == "Admin 2"
        assert admin3_db.nome == "Admin 3"

        assert admin1_db.email == "admin1@gmail.com"
        assert admin2_db.email == "admin2@gmail.com"
        assert admin3_db.email == "admin3@gmail.com"

    def test_importar_administrador_email_duplicado(self, test_db):
        """Testa importação de administrador com email duplicado"""
        # Arrange
        criar_tabela()
        admin1 = Administrador(
            id_admin=401,
            nome="Admin 1",
            email="duplicado@gmail.com",
            senha="12345678",
        )
        admin2 = Administrador(
            id_admin=402,  # ID diferente
            nome="Admin 2",
            email="duplicado@gmail.com",  # Email duplicado
            senha="87654321",
        )

        # Act
        resultado1 = importar(admin1)
        assert resultado1 is True

        # Assert - deve falhar por email único
        with pytest.raises(Exception):
            importar(admin2)
