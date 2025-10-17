import pytest
from datetime import datetime
from repo import chamado_repo
from repo import usuario_repo
from repo import administrador_repo
from model.chamado_model import Chamado
from model.usuario_model import Usuario
from model.administrador_model import Administrador
from model.enums import ChamadoStatus


class TestChamadoRepo:
    """Testes para o repositório de chamados"""

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """Setup executado antes de cada teste"""
        # Criar tabelas necessárias
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        chamado_repo.criar_tabela()

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
        self.id_usuario = usuario_repo.inserir(self.usuario)

        self.admin = Administrador(0, "Admin Silva", "admin@email.com", "senha456")
        self.id_admin = administrador_repo.inserir(self.admin)

    def test_criar_tabela(self, test_db):
        """Testa a criação da tabela de chamados"""
        # Arrange - já feito no setup
        # Act
        resultado = chamado_repo.criar_tabela()

        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_chamado_sucesso(self, test_db):
        """Testa inserção de chamado com sucesso"""
        # Arrange
        chamado = Chamado(
            id_chamado=0,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            titulo="Problema no sistema",
            descricao="O sistema está apresentando erro ao fazer login",
            status=ChamadoStatus.ABERTO,
            data=datetime.now(),
        )

        # Act
        id_inserido = chamado_repo.inserir(chamado)

        # Assert
        assert id_inserido is not None, "ID do chamado inserido não deveria ser None"
        assert id_inserido > 0, "ID deveria ser maior que zero"

        # Verificar se foi salvo corretamente
        chamado_db = chamado_repo.obter_por_id(id_inserido)
        assert chamado_db is not None, "Chamado deveria existir no banco"
        assert chamado_db.titulo == chamado.titulo
        assert chamado_db.descricao == chamado.descricao
        assert chamado_db.status == ChamadoStatus.ABERTO
        assert chamado_db.id_usuario == self.id_usuario
        assert chamado_db.id_admin == self.id_admin

    def test_inserir_chamado_sem_admin(self, test_db):
        """Testa inserção de chamado sem admin atribuído"""
        # Arrange
        chamado = Chamado(
            id_chamado=0,
            id_usuario=self.id_usuario,
            id_admin=None,  # Sem admin atribuído
            titulo="Dúvida sobre funcionalidade",
            descricao="Como faço para resetar minha senha?",
            status=ChamadoStatus.ABERTO,
            data=datetime.now(),
        )

        # Act
        id_inserido = chamado_repo.inserir(chamado)

        # Assert
        assert id_inserido is not None, "Deveria permitir inserir chamado sem admin"

        chamado_db = chamado_repo.obter_por_id(id_inserido)
        assert chamado_db.id_admin is None

    def test_atualizar_status_chamado_sucesso(self, test_db):
        """Testa atualização de status do chamado com sucesso"""
        # Arrange
        chamado = Chamado(
            id_chamado=0,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            titulo="Problema urgente",
            descricao="Sistema fora do ar",
            status=ChamadoStatus.ABERTO,
            data=datetime.now(),
        )
        id_chamado = chamado_repo.inserir(chamado)

        # Act - mudar para em andamento
        resultado = chamado_repo.atualizar_status(
            id_chamado, ChamadoStatus.EM_ANDAMENTO
        )

        # Assert
        assert resultado == True, "Atualização deveria retornar True"

        chamado_db = chamado_repo.obter_por_id(id_chamado)
        assert chamado_db.status == ChamadoStatus.EM_ANDAMENTO

        # Act - mudar para resolvido
        resultado = chamado_repo.atualizar_status(id_chamado, ChamadoStatus.RESOLVIDO)

        # Assert
        assert resultado == True
        chamado_db = chamado_repo.obter_por_id(id_chamado)
        assert chamado_db.status == ChamadoStatus.RESOLVIDO

    def test_atualizar_status_chamado_inexistente(self, test_db):
        """Testa atualização de status de chamado inexistente"""
        # Arrange
        id_inexistente = 9999

        # Act
        resultado = chamado_repo.atualizar_status(
            id_inexistente, ChamadoStatus.RESOLVIDO
        )

        # Assert
        assert (
            resultado == False
        ), "Atualização de chamado inexistente deveria retornar False"

    def test_excluir_chamado_sucesso(self, test_db):
        """Testa exclusão de chamado com sucesso"""
        # Arrange
        chamado = Chamado(
            id_chamado=0,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            titulo="Para excluir",
            descricao="Este chamado será excluído",
            status=ChamadoStatus.ABERTO,
            data=datetime.now(),
        )
        id_chamado = chamado_repo.inserir(chamado)

        # Act
        resultado = chamado_repo.excluir(id_chamado)

        # Assert
        assert resultado == True, "Exclusão deveria retornar True"

        chamado_db = chamado_repo.obter_por_id(id_chamado)
        assert chamado_db is None, "Chamado não deveria mais existir"

    def test_excluir_chamado_inexistente(self, test_db):
        """Testa exclusão de chamado inexistente"""
        # Arrange
        id_inexistente = 9999

        # Act
        resultado = chamado_repo.excluir(id_inexistente)

        # Assert
        assert (
            resultado == False
        ), "Exclusão de chamado inexistente deveria retornar False"

    def test_obter_todos_chamados_paginado(self, test_db):
        """Testa obtenção paginada de chamados"""
        # Arrange
        chamados = [
            Chamado(
                0,
                self.id_usuario,
                self.id_admin,
                "Erro no login",
                "Não consigo fazer login",
                ChamadoStatus.ABERTO,
                datetime.now(),
            ),
            Chamado(
                0,
                self.id_usuario,
                None,
                "Dúvida",
                "Como altero meu email?",
                ChamadoStatus.ABERTO,
                datetime.now(),
            ),
            Chamado(
                0,
                self.id_usuario,
                self.id_admin,
                "Bug crítico",
                "Sistema travando",
                ChamadoStatus.EM_ANDAMENTO,
                datetime.now(),
            ),
            Chamado(
                0,
                self.id_usuario,
                self.id_admin,
                "Sugestão",
                "Adicionar modo escuro",
                ChamadoStatus.RESOLVIDO,
                datetime.now(),
            ),
            Chamado(
                0,
                self.id_usuario,
                None,
                "Problema resolvido",
                "Já foi corrigido",
                ChamadoStatus.RESOLVIDO,
                datetime.now(),
            ),
        ]

        for chamado in chamados:
            chamado_repo.inserir(chamado)

        # Act - primeira página
        pagina1 = chamado_repo.obter_pagina(offset=0, limite=3)

        # Assert
        assert len(pagina1) == 3, "Primeira página deveria ter 3 chamados"

        # Act - segunda página
        pagina2 = chamado_repo.obter_pagina(offset=3, limite=3)

        # Assert
        assert len(pagina2) == 2, "Segunda página deveria ter 2 chamados"

    def test_obter_todos_chamados_paginado_vazio(self, test_db):
        """Testa obtenção paginada quando não há chamados"""
        # Arrange - sem inserir chamados adicionais
        # Act
        chamados = chamado_repo.obter_pagina(offset=0, limite=10)

        # Assert
        assert isinstance(chamados, list), "Deveria retornar uma lista"

    def test_obter_chamado_por_id_existente(self, test_db):
        """Testa obtenção de chamado por ID existente"""
        # Arrange
        chamado = Chamado(
            id_chamado=0,
            id_usuario=self.id_usuario,
            id_admin=self.id_admin,
            titulo="Teste de busca",
            descricao="Descrição do teste",
            status=ChamadoStatus.ABERTO,
            data=datetime.now(),
        )
        id_chamado = chamado_repo.inserir(chamado)

        # Act
        chamado_db = chamado_repo.obter_por_id(id_chamado)

        # Assert
        assert chamado_db is not None, "Chamado deveria existir"
        assert chamado_db.id_chamado == id_chamado
        assert chamado_db.titulo == chamado.titulo
        assert chamado_db.descricao == chamado.descricao
        assert chamado_db.status == chamado.status

    def test_obter_chamado_por_id_inexistente(self, test_db):
        """Testa obtenção de chamado por ID inexistente"""
        # Arrange
        id_inexistente = 9999

        # Act
        chamado = chamado_repo.obter_por_id(id_inexistente)

        # Assert
        assert chamado is None, "Chamado não deveria existir"

    def test_fluxo_completo_chamado(self, test_db):
        """Testa fluxo completo: criar, atualizar status e resolver chamado"""
        # Arrange
        chamado = Chamado(
            id_chamado=0,
            id_usuario=self.id_usuario,
            id_admin=None,  # Inicialmente sem admin
            titulo="Problema completo",
            descricao="Teste de fluxo completo",
            status=ChamadoStatus.ABERTO,
            data=datetime.now(),
        )

        # Act 1 - Criar chamado
        id_chamado = chamado_repo.inserir(chamado)
        assert id_chamado is not None

        # Act 2 - Admin pega o chamado (atualiza status)
        resultado = chamado_repo.atualizar_status(
            id_chamado, ChamadoStatus.EM_ANDAMENTO
        )
        assert resultado == True

        # Verificar status
        chamado_db = chamado_repo.obter_por_id(id_chamado)
        assert chamado_db.status == ChamadoStatus.EM_ANDAMENTO

        # Act 3 - Resolver chamado
        resultado = chamado_repo.atualizar_status(id_chamado, ChamadoStatus.RESOLVIDO)
        assert resultado == True

        # Verificar resolução
        chamado_db = chamado_repo.obter_por_id(id_chamado)
        assert chamado_db.status == ChamadoStatus.RESOLVIDO
