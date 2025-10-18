# from dataclasses import dataclass  # noqa: F401
# import os  # noqa: F401
# import sys  # noqa: F401
from datetime import date
from model.seguida_model import Seguida
from model.tutor_model import Tutor
from model.veterinario_model import Veterinario
# from model.usuario_model import Usuario  # noqa: F401
from repo.tutor_repo import (
    criar_tabela as criar_tabela_tutor,
    inserir as inserir_tutor,
)
from repo.veterinario_repo import (
    criar_tabela as criar_tabela_veterinario,
    inserir as inserir_veterinario,
)
from repo.usuario_repo import criar_tabela as criar_tabela_usuario
from repo.seguida_repo import (
    criar_tabela as criar_tabela_seguida,
    inserir as inserir_seguida,
    excluir as excluir_seguida,
    obter_pagina as obter_seguidas_paginado,
    obter_por_id as obter_seguida_por_id,
)
from repo import veterinario_repo, tutor_repo


class TestSeguidaRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_seguida()
        # Assert
        assert resultado is True, "A criação da tabela deveria retornar True"

    def test_inserir_seguida(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela_seguida()

        # Inserir veterinário
        vet = Veterinario(
            id_usuario=0,
            nome="Dr. João",
            email="vet@email.com",
            senha="123",
            telefone="999999999",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV123",
            verificado=True,
            bio="Especialista",
        )
        id_vet = inserir_veterinario(vet)

        # Inserir tutor
        tutor = Tutor(
            id_usuario=0,
            nome="Maria",
            email="maria@email.com",
            senha="321",
            telefone="888888888",
            perfil="tutor",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            quantidade_pets=0,
            descricao_pets=None,
        )
        id_tutor = inserir_tutor(tutor)

        # Criar seguida
        seguida_teste = Seguida(
            id_veterinario=id_vet, id_tutor=id_tutor, data_inicio=date.today()
        )

        # Act
        resultado = inserir_seguida(seguida_teste)

        # Assert
        assert resultado is True, "A inserção da seguida deveria retornar True"
        seguida_db = obter_seguida_por_id(id_vet, id_tutor)  # type: ignore[arg-type]  # noqa: E501
        assert (
            seguida_db is not None
        ), "A seguida inserida não deveria ser None"
        assert (
            seguida_db.id_veterinario == id_vet
        ), "O ID do veterinário inserido não confere"
        assert (
            seguida_db.id_tutor == id_tutor
        ), "O ID do tutor inserido não confere"

    def test_excluir_seguida(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela_seguida()

        # Inserir veterinário
        vet = Veterinario(
            id_usuario=0,
            nome="Dr. João",
            email="vet@email.com",
            senha="123",
            telefone="999999999",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV123",
            verificado=True,
            bio="Especialista",
        )
        id_vet = inserir_veterinario(vet)

        # Inserir tutor
        tutor = Tutor(
            id_usuario=0,
            nome="Maria",
            email="maria@email.com",
            senha="321",
            telefone="888888888",
            perfil="tutor",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            quantidade_pets=0,
            descricao_pets=None,
        )
        id_tutor = inserir_tutor(tutor)

        # Criar seguida
        seguida_teste = Seguida(
            id_veterinario=id_vet, id_tutor=id_tutor, data_inicio=date.today()
        )

        resultado1 = inserir_seguida(seguida_teste)

        # Act
        resultado2 = excluir_seguida(id_vet, id_tutor)  # type: ignore[arg-type]  # noqa: E501

        # Assert
        assert (
            resultado1 is True
        ), "A exclusão da seguida deveria retornar True"
        assert (
            resultado2 is True
        ), "A exclusão da seguida deveria retornar True"
        seguida_excluida = obter_seguida_por_id(id_vet, id_tutor)  # type: ignore[arg-type]  # noqa: E501
        assert seguida_excluida is None, "A seguida excluída deveria ser None"

    def test_obter_todas_seguidas_paginado(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela_seguida()

        # Cria uma coleção com 10 veterinários
        veterinarios = []
        for i in range(10):
            veterinario = Veterinario(
                id_usuario=0,
                nome=f"Veterinário {i+1}",
                email=f"vet{i+1}@email.com",
                senha="123",
                telefone="999999999",
                perfil="veterinario",
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                crmv="CRMV123",
                verificado=True,
                bio="Especialista",
            )
            veterinarios.append(veterinario)

        # Cria uma coleção com 10 tutores
        tutores = []
        for i in range(10):
            tutor = Tutor(
                id_usuario=0,
                nome=f"Tutor {i+1}",
                email=f"tutor{i+1}@email.com",
                senha="321",
                telefone="888888888",
                perfil="tutor",
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                quantidade_pets=0,
                descricao_pets=None,
            )
            tutores.append(tutor)

        for i in range(10):
            inserir_veterinario(veterinarios[i])
            inserir_tutor(tutores[i])

        veterinarios_bd = veterinario_repo.obter_pagina(10, 0)
        tutores_bd = tutor_repo.obter_pagina(10, 0)
        seguidas = []
        for i in range(10):
            seguida_teste = Seguida(
                id_veterinario=veterinarios_bd[i].id_usuario,
                id_tutor=tutores_bd[i].id_usuario,
                data_inicio=date.today(),
            )
            seguidas.append(seguida_teste)

        for seguida in seguidas:
            inserir_seguida(seguida)

        # Act
        seguidas = obter_seguidas_paginado(1, 4)

        # Assert
        assert len(seguidas) == 4, "Deveria retornar quatro seguidas"

    def test_obter_seguida_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela_seguida()

        # Inserir veterinário
        vet = Veterinario(
            id_usuario=0,
            nome="Dr. João",
            email="vet@email.com",
            senha="123",
            telefone="999999999",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV123",
            verificado=True,
            bio="Especialista",
        )
        id_vet = inserir_veterinario(vet)

        # Inserir tutor
        tutor = Tutor(
            id_usuario=0,
            nome="Maria",
            email="maria@email.com",
            senha="321",
            telefone="888888888",
            perfil="tutor",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            quantidade_pets=0,
            descricao_pets=None,
        )
        id_tutor = inserir_tutor(tutor)

        # Criar seguida (usando apenas os IDs, não os objetos completos)
        seguida_teste = Seguida(
            id_veterinario=id_vet, id_tutor=id_tutor, data_inicio=date.today()
        )

        # Inserir seguida
        inserir_seguida(seguida_teste)

        # Act
        seguida_db = obter_seguida_por_id(id_vet, id_tutor)  # type: ignore[arg-type]  # noqa: E501

        # Assert
        assert seguida_db is not None, "A seguida obtida não deveria ser None"
        assert (
            seguida_db.id_veterinario == id_vet
        ), "O ID do veterinário obtido não confere"
        assert (
            seguida_db.id_tutor == id_tutor
        ), "O ID do tutor obtido não confere"
        assert (
            seguida_db.data_inicio is not None
        ), "A data de início não deveria ser None"
        # Verificar se os IDs estão corretos
        # (modelo simplificado sem objetos relacionados)
        # Para verificar os objetos relacionados,
        # seria necessário fazer consultas separadas

    def test_obter_seguida_inexistente(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela_seguida()
        # Act
        seguida_db = obter_seguida_por_id(999, 888)
        # Assert
        assert (
            seguida_db is None
        ), "A seguida inexistente deveria retornar None"

    def test_excluir_seguida_inexistente(self, test_db):
        """Testa exclusão de seguida inexistente"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela_seguida()

        # Act
        resultado = excluir_seguida(9999, 9999)

        # Assert
        assert (
            resultado is False
        ), "Exclusão de seguida inexistente deveria retornar False"

    def test_obter_seguidas_paginado_vazio(self, test_db):
        """Testa obtenção paginada quando não há seguidas"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela_seguida()

        # Act
        seguidas = obter_seguidas_paginado(pagina=1, tamanho_pagina=10)

        # Assert
        assert len(seguidas) == 0, "Deveria retornar lista vazia"

    def test_inserir_seguida_duplicada(self, test_db):
        """Testa inserção de seguida duplicada.
        Deveria falhar por constraint.
        """
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela_seguida()

        vet = Veterinario(
            0,
            "Dr. Silva",
            "silva@vet.com",
            "123",
            "999999999",
            "veterinario",
            None,
            None,
            None,
            None,
            "CRMV111",
            True,
            "Bio",
        )
        id_vet = inserir_veterinario(vet)

        tutor = Tutor(
            0,
            "João",
            "joao@email.com",
            "321",
            "888888888",
            "tutor",
            None,
            None,
            None,
            None,
            1,
            "Cachorro",
        )
        id_tutor = inserir_tutor(tutor)

        seguida = Seguida(id_vet, id_tutor, date.today())  # type: ignore[arg-type]  # noqa: E501
        inserir_seguida(seguida)

        # Act - tentar inserir novamente
        resultado = inserir_seguida(seguida)

        # Assert
        assert (
            resultado is False
        ), "Inserção de seguida duplicada deveria retornar False"
