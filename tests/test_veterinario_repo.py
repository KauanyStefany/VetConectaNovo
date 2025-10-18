# import os  # noqa: F401
# import sys  # noqa: F401
from repo.veterinario_repo import (
    criar_tabela as criar_tabela_veterinario,
    inserir as inserir_veterinario,
    atualizar as atualizar_veterinario,
    atualizar_verificacao,
    excluir as excluir_veterinario,
    obter_pagina as obter_por_pagina,
    obter_por_id,
)
from model.veterinario_model import Veterinario
# from model.usuario_model import Usuario  # noqa: F401
from repo.usuario_repo import criar_tabela as criar_tabela_usuario


class TestVeterinarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_veterinario()
        # Assert
        assert (
            resultado is True
        ), "A criação da tabela de veterinários deveria retornar True"

    def test_inserir_veterinario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        novo_veterinario = Veterinario(
            id_usuario=0,
            nome="Veterinario Teste",
            email="vet@gmail.com",
            senha="senha123",
            telefone="11999999999",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste",
        )
        # Insere um usuário para a FK id_usuario
        id_novo_veterinario = inserir_veterinario(novo_veterinario)
        # Act
        # Assert
        assert (
            id_novo_veterinario is not None
        ), "A inserção do veterinário deveria retornar um ID válido"
        veterinario_db = obter_por_id(id_novo_veterinario)  # type: ignore[arg-type]  # noqa: E501
        assert (
            veterinario_db is not None
        ), "O veterinário inserido não deveria ser None"
        assert (
            veterinario_db.id_usuario == id_novo_veterinario
        ), "O ID do veterinário inserido não confere"
        assert (
            veterinario_db.nome == "Veterinario Teste"
        ), "O nome do veterinário inserido não confere"
        assert (
            veterinario_db.email == "vet@gmail.com"
        ), "O email do veterinário inserido não confere"
        # Senha não é retornada por segurança
        assert (
            veterinario_db.telefone == "11999999999"
        ), "O telefone do veterinário inserido não confere"
        assert (
            veterinario_db.crmv == "SP-123456"
        ), "O CRMV do veterinário inserido não confere"
        assert (
            veterinario_db.verificado == False  # noqa: E712
        ), "O status de verificado do veterinário inserido não confere"
        assert (
            veterinario_db.bio == "Veterinário para teste"
        ), "A bio do veterinário inserido não confere"

    def test_atualizar_veterinario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        novo_veterinario = Veterinario(
            id_usuario=0,
            nome="Veterinario Teste",
            email="vet@gmail.com",
            senha="senha123",
            telefone="11999999999",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste",
        )
        id_novo_veterinario = inserir_veterinario(novo_veterinario)
        veterinario_inserido = obter_por_id(id_novo_veterinario)  # type: ignore[arg-type]  # noqa: E501
        assert veterinario_inserido is not None

        # Act
        # Atualizando atributos herdados do usuário
        veterinario_inserido.nome = "Dr. Atualizado"
        veterinario_inserido.email = "atualizado@example.com"
        veterinario_inserido.telefone = "11988888888"
        # Atualizando atributos exclusivos do veterinário
        veterinario_inserido.crmv = "SP-654321"
        veterinario_inserido.verificado = True
        veterinario_inserido.bio = "Bio atualizada"
        # Chama a função de atualização
        resultado = atualizar_veterinario(veterinario_inserido)

        # Assert
        assert (
            resultado is True
        ), "A atualização do veterinário deveria retornar True"
        veterinario_db = obter_por_id(id_novo_veterinario)  # type: ignore[arg-type]  # noqa: E501
        assert veterinario_db is not None
        assert (
            veterinario_db.nome == "Dr. Atualizado"
        ), "O nome do veterinário não foi atualizado corretamente"
        assert (
            veterinario_db.email == "atualizado@example.com"
        ), "O email do veterinário não foi atualizado corretamente"
        assert (
            veterinario_db.telefone == "11988888888"
        ), "O telefone do veterinário não foi atualizado corretamente"
        assert (
            veterinario_db.crmv == "SP-654321"
        ), "O CRMV do veterinário não foi atualizado corretamente"
        assert (
            veterinario_db.verificado == True  # noqa: E712
        ), "O status de verificado não foi atualizado corretamente"
        assert (
            veterinario_db.bio == "Bio atualizada"
        ), "A bio do veterinário não foi atualizada corretamente"

    def test_excluir_veterinario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        novo_veterinario = Veterinario(
            id_usuario=0,
            nome="Veterinario Teste",
            email="vet@gmail",
            senha="senha123",
            telefone="11999999999",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste",
        )
        id_novo_veterinario = inserir_veterinario(novo_veterinario)
        # act
        resultado = excluir_veterinario(id_novo_veterinario)  # type: ignore[arg-type]  # noqa: E501
        # Assert
        assert (
            resultado is True
        ), "A exclusão do veterinário deveria retornar True"
        veterinario_excluido = obter_por_id(id_novo_veterinario)  # type: ignore[arg-type]  # noqa: E501
        assert (
            veterinario_excluido is None
        ), "O veterinário excluído deveria ser None"

    def test_obter_todos_veterinarios(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        vet1 = Veterinario(
            id_usuario=0,
            nome="Veterinario Teste",
            email="vet@gmail.com",
            senha="senha123",
            telefone="11999999999",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste",
        )
        vet2 = Veterinario(
            id_usuario=1,
            nome="Dr. B",
            email="b@example.com",
            senha="senhaB",
            telefone="22222222222",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV-B",
            verificado=True,
            bio="Veterinário B",
        )
        inserir_veterinario(vet1)
        inserir_veterinario(vet2)

        # Act
        veterinarios_db = obter_por_pagina(2, 0)
        # Assert
        assert len(veterinarios_db) == 2, "Deveriam ser obtidos 2 veterinários"
        assert (
            veterinarios_db[0].nome == "Veterinario Teste"
        ), "O nome do primeiro veterinário obtido não confere"
        assert (
            veterinarios_db[1].nome == "Dr. B"
        ), "O nome do segundo veterinário obtido não confere"

    def test_obter_veterinario_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        veterinario_teste = Veterinario(
            id_usuario=1,
            nome="Dr. Teste",
            email="vet@gmail.com",
            senha="senha123",
            telefone="11999999999",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste",
        )
        inserir_veterinario(veterinario_teste)
        # Act
        veterinario_db = obter_por_id(1)
        # Assert
        assert (
            veterinario_db is not None
        ), "O veterinário obtido não deveria ser None"
        assert (
            veterinario_db.id_usuario == veterinario_teste.id_usuario
        ), "O ID do veterinário obtido não confere"
        assert (
            veterinario_db.nome == "Dr. Teste"
        ), "O nome do veterinário obtido não confere"
        assert (
            veterinario_db.crmv == "SP-123456"
        ), "O CRMV do veterinário obtido não confere"
        assert (
            veterinario_db.bio == "Veterinário para teste"
        ), "A bio do veterinário obtido não confere"

    def test_atualizar_verificacao_sucesso(self, test_db):
        """Testa atualização do status de verificação do veterinário"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        novo_veterinario = Veterinario(
            id_usuario=0,
            nome="Dr. Não Verificado",
            email="nao.verificado@vet.com",
            senha="senha123",
            telefone="11999999999",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="SP-999999",
            verificado=False,
            bio="Veterinário aguardando verificação",
        )
        id_veterinario = inserir_veterinario(novo_veterinario)

        # Act
        resultado = atualizar_verificacao(id_veterinario, True)  # type: ignore[arg-type]  # noqa: E501

        # Assert
        assert (
            resultado is True
        ), "Atualização de verificação deveria retornar True"
        veterinario_db = obter_por_id(id_veterinario)  # type: ignore[arg-type]
        assert veterinario_db is not None
        assert (
            veterinario_db.verificado == True  # noqa: E712
        ), "Status de verificado deveria ser True"

    def test_atualizar_verificacao_veterinario_inexistente(self, test_db):
        """Testa atualização de verificação com veterinário inexistente"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        id_inexistente = 9999

        # Act
        resultado = atualizar_verificacao(id_inexistente, True)  # type: ignore[arg-type]  # noqa: E501

        # Assert
        assert resultado is False, (
            "Atualização de verificação de veterinário inexistente "
            "deveria retornar False"
        )
