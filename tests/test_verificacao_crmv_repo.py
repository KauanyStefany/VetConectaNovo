import pytest
from datetime import datetime
from repo.verificacao_crmv_repo import (
    criar_tabela as criar_tabela_verificacao,
    inserir,
    atualizar,
    excluir,
    obter_pagina,
    obter_por_id,
)
from repo.usuario_repo import criar_tabela as criar_tabela_usuario, inserir as inserir_usuario
from repo.veterinario_repo import criar_tabela as criar_tabela_veterinario, inserir as inserir_veterinario
from repo.administrador_repo import criar_tabela as criar_tabela_admin, inserir as inserir_admin
from model.verificacao_crmv_model import VerificacaoCRMV
from model.veterinario_model import Veterinario
from model.administrador_model import Administrador
from model.usuario_model import Usuario
from model.enums import VerificacaoStatus


class TestVerificacaoCRMVRepo:
    """Testes para o repositório de verificação CRMV"""

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """Setup executado antes de cada teste"""
        # Criar tabelas necessárias
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_admin()
        criar_tabela_verificacao()

        # Criar dados base para os testes
        self.veterinario = Veterinario(
            id_usuario=0,
            nome="Dr. João Silva",
            email="dr.joao@email.com",
            senha="senha123",
            telefone="11999998888",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="SP-12345",
            verificado=False,
            bio="Veterinário clínico geral",
        )
        self.id_veterinario = inserir_veterinario(self.veterinario)

        self.admin = Administrador(0, "Admin Silva", "admin@email.com", "senha456")
        self.id_admin = inserir_admin(self.admin)

    def test_criar_tabela(self, test_db):
        """Testa a criação da tabela de verificação CRMV"""
        # Arrange - já feito no setup
        # Act
        resultado = criar_tabela_verificacao()

        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_verificacao_sucesso(self, test_db):
        """Testa inserção de verificação CRMV com sucesso"""
        # Arrange
        verificacao = VerificacaoCRMV(
            id_verificacao_crmv=0,
            id_veterinario=self.id_veterinario,
            id_administrador=self.id_admin,
            data_verificacao=datetime.now(),
            status_verificacao=VerificacaoStatus.PENDENTE,
        )

        # Act
        id_inserido = inserir(verificacao)

        # Assert
        assert (
            id_inserido is not None
        ), "ID da verificação inserida não deveria ser None"
        assert id_inserido > 0, "ID deveria ser maior que zero"

        # Verificar se foi salvo corretamente
        verificacao_db = obter_por_id(id_inserido)
        assert verificacao_db is not None, "Verificação deveria existir no banco"
        assert verificacao_db.id_veterinario == self.id_veterinario
        assert verificacao_db.id_administrador == self.id_admin
        assert verificacao_db.status_verificacao == VerificacaoStatus.PENDENTE

    def test_inserir_verificacao_sem_admin(self, test_db):
        """Testa inserção de verificação CRMV sem admin atribuído"""
        # Arrange - Agora id_administrador pode ser NULL
        verificacao = VerificacaoCRMV(
            id_verificacao_crmv=0,
            id_veterinario=self.id_veterinario,
            id_administrador=None,  # Sem admin atribuído
            data_verificacao=datetime.now(),
            status_verificacao=VerificacaoStatus.PENDENTE,
        )

        # Act
        id_inserido = inserir(verificacao)

        # Assert
        assert id_inserido is not None, "Deveria permitir inserir verificação sem admin"

        verificacao_db = obter_por_id(id_inserido)
        assert verificacao_db.id_administrador is None

    def test_atualizar_status_verificacao_sucesso(self, test_db):
        """Testa atualização de status da verificação CRMV com sucesso"""
        # Arrange
        verificacao_original = VerificacaoCRMV(
            id_verificacao_crmv=0,
            id_veterinario=self.id_veterinario,
            id_administrador=self.id_admin,
            data_verificacao=datetime.now(),
            status_verificacao=VerificacaoStatus.PENDENTE,
        )
        id_verificacao = inserir(verificacao_original)

        # Act - aprovar verificação
        resultado = atualizar(
            self.id_veterinario, VerificacaoStatus.APROVADO, self.id_admin
        )

        # Assert
        assert resultado == True, "Atualização deveria retornar True"

        verificacao_db = obter_por_id(id_verificacao)
        assert verificacao_db.status_verificacao == VerificacaoStatus.APROVADO

        # Act - rejeitar verificação
        resultado = atualizar(
            self.id_veterinario, VerificacaoStatus.REJEITADO, self.id_admin
        )

        # Assert
        assert resultado == True
        verificacao_db = obter_por_id(id_verificacao)
        assert verificacao_db.status_verificacao == VerificacaoStatus.REJEITADO

    def test_atualizar_verificacao_inexistente(self, test_db):
        """Testa atualização de verificação inexistente"""
        # Arrange
        id_inexistente = 9999

        # Act
        resultado = atualizar(id_inexistente, VerificacaoStatus.APROVADO, self.id_admin)

        # Assert
        assert (
            resultado == False
        ), "Atualização de verificação inexistente deveria retornar False"

    def test_excluir_verificacao_sucesso(self, test_db):
        """Testa exclusão de verificação CRMV com sucesso"""
        # Arrange
        verificacao = VerificacaoCRMV(
            id_verificacao_crmv=0,
            id_veterinario=self.id_veterinario,
            id_administrador=self.id_admin,
            data_verificacao=datetime.now(),
            status_verificacao=VerificacaoStatus.PENDENTE,
        )
        id_verificacao = inserir(verificacao)

        # Act
        resultado = excluir(self.id_veterinario)

        # Assert
        assert resultado == True, "Exclusão deveria retornar True"

        verificacao_db = obter_por_id(id_verificacao)
        assert verificacao_db is None, "Verificação não deveria mais existir"

    def test_excluir_verificacao_inexistente(self, test_db):
        """Testa exclusão de verificação inexistente"""
        # Arrange
        id_inexistente = 9999

        # Act
        resultado = excluir(id_inexistente)

        # Assert
        assert (
            resultado == False
        ), "Exclusão de verificação inexistente deveria retornar False"

    def test_OBTER_PAGINA(self, test_db):
        """Testa obtenção paginada de verificações CRMV"""
        # Arrange - criar verificações simples usando o mesmo veterinário
        verificacoes_ids = []
        for i in range(5):
            verificacao = VerificacaoCRMV(
                0,
                self.id_veterinario,
                self.id_admin,
                datetime.now(),
                VerificacaoStatus.PENDENTE,
            )
            verificacoes_ids.append(inserir(verificacao))

        # Act - primeira página
        pagina1 = obter_pagina(limite=3, offset=0)

        # Assert
        assert len(pagina1) == 3, "Primeira página deveria ter 3 verificações"

        # Act - segunda página
        pagina2 = obter_pagina(limite=3, offset=3)

        # Assert
        assert len(pagina2) == 2, "Segunda página deveria ter 2 verificações"

    def test_OBTER_PAGINA_vazio(self, test_db):
        """Testa obtenção paginada quando não há verificações"""
        # Arrange - sem inserir verificações adicionais
        # Act
        verificacoes = obter_pagina(limite=10, offset=0)

        # Assert
        assert isinstance(verificacoes, list), "Deveria retornar uma lista"
        assert len(verificacoes) == 0, "Lista deveria estar vazia"

    def test_obter_por_id_existente(self, test_db):
        """Testa obtenção de verificação por ID existente"""
        # Arrange
        verificacao = VerificacaoCRMV(
            id_verificacao_crmv=0,
            id_veterinario=self.id_veterinario,
            id_administrador=self.id_admin,
            data_verificacao=datetime.now(),
            status_verificacao=VerificacaoStatus.PENDENTE,
        )
        id_verificacao = inserir(verificacao)

        # Act
        verificacao_db = obter_por_id(id_verificacao)

        # Assert
        assert verificacao_db is not None, "Verificação deveria existir"
        assert verificacao_db.id_verificacao_crmv == id_verificacao
        assert verificacao_db.id_veterinario == self.id_veterinario
        assert verificacao_db.status_verificacao == VerificacaoStatus.PENDENTE

    def test_obter_por_id_inexistente(self, test_db):
        """Testa obtenção de verificação por ID inexistente"""
        # Arrange
        id_inexistente = 9999

        # Act
        verificacao = obter_por_id(id_inexistente)

        # Assert
        assert verificacao is None, "Verificação não deveria existir"

    def test_fluxo_completo_verificacao(self, test_db):
        """Testa fluxo completo: criar, aprovar verificação CRMV"""
        # Arrange
        verificacao = VerificacaoCRMV(
            id_verificacao_crmv=0,
            id_veterinario=self.id_veterinario,
            id_administrador=None,  # Inicialmente sem admin
            data_verificacao=datetime.now(),
            status_verificacao=VerificacaoStatus.PENDENTE,
        )

        # Act 1 - Criar verificação
        id_verificacao = inserir(verificacao)
        assert id_verificacao is not None

        # Act 2 - Admin analisa e aprova
        resultado = atualizar(
            self.id_veterinario, VerificacaoStatus.APROVADO, self.id_admin
        )
        assert resultado == True

        # Verificar aprovação
        verificacao_db = obter_por_id(id_verificacao)
        assert verificacao_db.status_verificacao == VerificacaoStatus.APROVADO

    def test_enum_status_valores(self, test_db):
        """Testa se os valores dos enums estão corretos"""
        # Arrange - usar apenas o veterinário existente
        statuses = [
            VerificacaoStatus.PENDENTE,
            VerificacaoStatus.APROVADO,
            VerificacaoStatus.REJEITADO,
        ]
        ids_verificacao = []

        for status in statuses:
            verificacao = VerificacaoCRMV(
                0, self.id_veterinario, self.id_admin, datetime.now(), status
            )
            ids_verificacao.append(inserir(verificacao))

        # Act & Assert
        verificacao1 = obter_por_id(ids_verificacao[0])
        assert verificacao1.status_verificacao == VerificacaoStatus.PENDENTE

        verificacao2 = obter_por_id(ids_verificacao[1])
        assert verificacao2.status_verificacao == VerificacaoStatus.APROVADO

        verificacao3 = obter_por_id(ids_verificacao[2])
        assert verificacao3.status_verificacao == VerificacaoStatus.REJEITADO
