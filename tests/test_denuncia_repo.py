import pytest
from datetime import datetime
from repo.denuncia_repo import (
    criar_tabela as criar_tabela_denuncia,
    inserir as inserir_denuncia,
    atualizar as atualizar_denuncia,
    excluir as excluir_denuncia,
    obter_pagina as obter_todas_denuncias_paginadas,
    obter_por_id as obter_denuncia_por_id
)
from repo.usuario_repo import (
    criar_tabela as criar_tabela_usuario,
    inserir as inserir_usuario
)
from repo.administrador_repo import (
    criar_tabela,
    inserir
)
from model.denuncia_model import Denuncia
from model.usuario_model import Usuario
from model.administrador_model import Administrador
from model.enums import DenunciaStatus


class TestDenunciaRepo:
    """Testes para o repositório de denúncias"""

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """Setup executado antes de cada teste"""
        # Criar tabelas necessárias
        criar_tabela_usuario()
        criar_tabela()
        criar_tabela_denuncia()

        # Criar dados base para os testes
        self.usuario = Usuario(
            0,
            "João Silva",
            "joao@email.com",
            "senha123",
            "11999998888",
            "tutor",
            None,
            None,
            None,
            None,
        )
        self.id_usuario = inserir_usuario(self.usuario)

        self.admin = Administrador(0, "Admin Silva", "admin@email.com", "senha456")
        self.id_admin = inserir(self.admin)

    def test_criar_tabela(self, test_db):
        """Testa a criação da tabela de denúncias"""
        # Arrange - já feito no setup
        # Act
        resultado = criar_tabela_denuncia()

        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_denuncia_sucesso(self, test_db):
        """Testa inserção de denúncia com sucesso"""
        # Arrange
        denuncia = Denuncia(
            id_denuncia=0,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            motivo="Conteúdo inapropriado",
            data_denuncia=datetime.now(),
            status=DenunciaStatus.PENDENTE,
        )

        # Act
        id_inserido = inserir_denuncia(denuncia)

        # Assert
        assert id_inserido is not None, "ID da denúncia inserida não deveria ser None"
        assert id_inserido > 0, "ID deveria ser maior que zero"

        # Verificar se foi salvo corretamente
        denuncia_db = obter_denuncia_por_id(id_inserido)
        assert denuncia_db is not None, "Denúncia deveria existir no banco"
        assert denuncia_db.motivo == denuncia.motivo
        assert denuncia_db.status == DenunciaStatus.PENDENTE
        assert denuncia_db.id_usuario == self.id_usuario
        assert denuncia_db.id_admin == self.id_admin

    def test_inserir_denuncia_sem_admin(self, test_db):
        """Testa inserção de denúncia sem admin atribuído"""
        # Arrange
        denuncia = Denuncia(
            id_denuncia=0,
            id_usuario=self.id_usuario,
            id_admin=None,  # Sem admin atribuído
            motivo="Spam",
            data_denuncia=datetime.now(),
            status=DenunciaStatus.PENDENTE,
        )

        # Act
        id_inserido = inserir_denuncia(denuncia)

        # Assert
        assert id_inserido is not None, "Deveria permitir inserir denúncia sem admin"

        denuncia_db = obter_denuncia_por_id(id_inserido)
        assert denuncia_db is not None, "Denúncia deveria ter sido inserida"
        assert denuncia_db.id_admin is None

    def test_atualizar_denuncia_sucesso(self, test_db):
        """Testa atualização de denúncia com sucesso"""
        # Arrange
        denuncia_original = Denuncia(
            id_denuncia=0,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            motivo="Motivo original",
            data_denuncia=datetime.now(),
            status=DenunciaStatus.PENDENTE,
        )
        id_denuncia = inserir_denuncia(denuncia_original)

        # Act
        denuncia_atualizada = Denuncia(
            id_denuncia=id_denuncia,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            motivo="Motivo atualizado",
            data_denuncia=datetime.now(),
            status=DenunciaStatus.RESOLVIDA,
        )
        resultado = atualizar_denuncia(denuncia_atualizada)

        # Assert
        assert resultado == True, "Atualização deveria retornar True"

        denuncia_db = obter_denuncia_por_id(id_denuncia)
        assert denuncia_db.motivo == "Motivo atualizado"
        assert denuncia_db.status == DenunciaStatus.RESOLVIDA

    def test_atualizar_denuncia_inexistente(self, test_db):
        """Testa atualização de denúncia inexistente"""
        # Arrange
        denuncia_inexistente = Denuncia(
            id_denuncia=9999,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            motivo="Não existe",
            data_denuncia=datetime.now(),
            status=DenunciaStatus.PENDENTE,
        )

        # Act
        resultado = atualizar_denuncia(denuncia_inexistente)

        # Assert
        assert (
            resultado == False
        ), "Atualização de denúncia inexistente deveria retornar False"

    def test_excluir_denuncia_sucesso(self, test_db):
        """Testa exclusão de denúncia com sucesso"""
        # Arrange
        denuncia = Denuncia(
            id_denuncia=0,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            motivo="Para excluir",
            data_denuncia=datetime.now(),
            status=DenunciaStatus.PENDENTE,
        )
        id_denuncia = inserir_denuncia(denuncia)

        # Act
        resultado = excluir_denuncia(id_denuncia)

        # Assert
        assert resultado == True, "Exclusão deveria retornar True"

        denuncia_db = obter_denuncia_por_id(id_denuncia)
        assert denuncia_db is None, "Denúncia não deveria mais existir"

    def test_excluir_denuncia_inexistente(self, test_db):
        """Testa exclusão de denúncia inexistente"""
        # Arrange
        id_inexistente = 9999

        # Act
        resultado = excluir_denuncia(id_inexistente)

        # Assert
        assert (
            resultado == False
        ), "Exclusão de denúncia inexistente deveria retornar False"

    def test_obter_todas_denuncias_paginadas(self, test_db):
        """Testa obtenção paginada de denúncias"""
        # Arrange
        denuncias = [
            Denuncia(
                0,
                self.id_usuario,
                self.id_admin,
                "Motivo 1",
                datetime.now(),
                DenunciaStatus.PENDENTE,
            ),
            Denuncia(
                0,
                self.id_usuario,
                None,
                "Motivo 2",
                datetime.now(),
                DenunciaStatus.RESOLVIDA,
            ),
            Denuncia(
                0,
                self.id_usuario,
                self.id_admin,
                "Motivo 3",
                datetime.now(),
                DenunciaStatus.REJEITADA,
            ),
            Denuncia(
                0,
                self.id_usuario,
                None,
                "Motivo 4",
                datetime.now(),
                DenunciaStatus.PENDENTE,
            ),
            Denuncia(
                0,
                self.id_usuario,
                self.id_admin,
                "Motivo 5",
                datetime.now(),
                DenunciaStatus.RESOLVIDA,
            ),
        ]

        for denuncia in denuncias:
            inserir_denuncia(denuncia)

        # Act - primeira página
        pagina1 = obter_todas_denuncias_paginadas(limite=3, offset=0)

        # Assert
        assert len(pagina1) == 3, "Primeira página deveria ter 3 denúncias"

        # Act - segunda página
        pagina2 = obter_todas_denuncias_paginadas(limite=3, offset=3)

        # Assert
        assert len(pagina2) == 2, "Segunda página deveria ter 2 denúncias"

    def test_obter_todas_denuncias_paginadas_vazio(self, test_db):
        """Testa obtenção paginada quando não há denúncias"""
        # Arrange - sem inserir denúncias adicionais
        # Act
        denuncias = obter_todas_denuncias_paginadas(limite=10, offset=0)

        # Assert
        assert isinstance(denuncias, list), "Deveria retornar uma lista"
        assert len(denuncias) == 0, "Lista deveria estar vazia"

    def test_obter_denuncia_por_id_existente(self, test_db):
        """Testa obtenção de denúncia por ID existente"""
        # Arrange
        denuncia = Denuncia(
            id_denuncia=0,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            motivo="Teste de busca",
            data_denuncia=datetime.now(),
            status=DenunciaStatus.PENDENTE,
        )
        id_denuncia = inserir_denuncia(denuncia)

        # Act
        denuncia_db = obter_denuncia_por_id(id_denuncia)

        # Assert
        assert denuncia_db is not None, "Denúncia deveria existir"
        assert denuncia_db.id_denuncia == id_denuncia
        assert denuncia_db.motivo == denuncia.motivo
        assert denuncia_db.status == denuncia.status

    def test_obter_denuncia_por_id_inexistente(self, test_db):
        """Testa obtenção de denúncia por ID inexistente"""
        # Arrange
        id_inexistente = 9999

        # Act
        denuncia = obter_denuncia_por_id(id_inexistente)

        # Assert
        assert denuncia is None, "Denúncia não deveria existir"

    def test_fluxo_completo_denuncia(self, test_db):
        """Testa fluxo completo: criar, atualizar e resolver denúncia"""
        # Arrange
        denuncia = Denuncia(
            id_denuncia=0,
            id_usuario=self.id_usuario,
            id_admin=None,  # Inicialmente sem admin
            motivo="Conteúdo inadequado",
            data_denuncia=datetime.now(),
            status=DenunciaStatus.PENDENTE,
        )

        # Act 1 - Criar denúncia
        id_denuncia = inserir_denuncia(denuncia)
        assert id_denuncia is not None

        # Act 2 - Admin analisa a denúncia
        denuncia_atualizada = Denuncia(
            id_denuncia=id_denuncia,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,  # Agora com admin
            motivo="Conteúdo inadequado",
            data_denuncia=datetime.now(),
            status=DenunciaStatus.RESOLVIDA,
        )
        resultado = atualizar_denuncia(denuncia_atualizada)
        assert resultado == True

        # Verificar aprovação
        denuncia_db = obter_denuncia_por_id(id_denuncia)
        assert denuncia_db.status == DenunciaStatus.RESOLVIDA
        assert denuncia_db.id_admin == self.id_admin

    def test_enum_status_valores(self, test_db):
        """Testa se os valores dos enums estão corretos"""
        # Arrange
        denuncias = [
            Denuncia(
                0,
                self.id_usuario,
                self.id_admin,
                "Teste 1",
                datetime.now(),
                DenunciaStatus.PENDENTE,
            ),
            Denuncia(
                0,
                self.id_usuario,
                self.id_admin,
                "Teste 2",
                datetime.now(),
                DenunciaStatus.RESOLVIDA,
            ),
            Denuncia(
                0,
                self.id_usuario,
                self.id_admin,
                "Teste 3",
                datetime.now(),
                DenunciaStatus.REJEITADA,
            ),
        ]

        ids = []
        for denuncia in denuncias:
            ids.append(inserir_denuncia(denuncia))

        # Act & Assert
        denuncia1 = obter_denuncia_por_id(ids[0])
        assert denuncia1.status == DenunciaStatus.PENDENTE

        denuncia2 = obter_denuncia_por_id(ids[1])
        assert denuncia2.status == DenunciaStatus.RESOLVIDA

        denuncia3 = obter_denuncia_por_id(ids[2])
        assert denuncia3.status == DenunciaStatus.REJEITADA
