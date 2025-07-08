import os
import sys
from datetime import date

from model.administrador_model import *
from repo.administrador_repo import *
from model.chamado_model import Chamado
from repo.chamado_repo import *
from model.usuario_model import Usuario
from repo.usuario_repo import *
from model.resposta_chamado_model import RespostaChamado
from repo.resposta_chamado_repo import *
from repo.administrador_repo import criar_tabela_administrador, inserir_administrador
from model.administrador_model import Administrador

class TestRespostaChamadoRepo:
    
    def test_criar_tabelas(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabelas()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_resposta(self, test_db):
        # Arrange
        # Cria tabelas necessárias no banco temporário
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela_chamado()  # cria tabela chamado
        criar_tabelas()  # cria tabela resposta_chamado

        # Insere usuário dummy e obtém ID
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)

        # Insere administrador dummy e obtém ID
        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = inserir_administrador(admin_teste)

        # Cria chamado usando IDs válidos
        chamado_teste = Chamado(
            id_chamado=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )
        id_chamado_inserido = inserir_chamado(chamado_teste)

        # Cria resposta usando ID do chamado válido
        resposta_teste = RespostaChamado(
            id_resposta_chamado=None,
            id_chamado=id_chamado_inserido,
            titulo="Resposta ao chamado",
            descricao="Esta é uma resposta ao chamado",
            data=date(2025, 6, 30)
        )

        # Act
        id_resposta_inserida = inserir_resposta(resposta_teste)

        # Assert
        resposta_db = obter_resposta_por_id(id_resposta_inserida)
        assert resposta_db is not None, "A resposta inserida não deveria ser None"
        assert resposta_db.id_chamado == id_chamado_inserido, "O id do chamado não confere"
        assert resposta_db.titulo == "Resposta ao chamado", "O título da resposta não confere"
        assert resposta_db.descricao == "Esta é uma resposta ao chamado", "A descrição da resposta não confere"
        assert str(resposta_db.data) == "2025-06-30", "A data da resposta não confere"

    def test_atualizar_resposta(self, test_db):
        # Arrange
        # Cria tabelas necessárias
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela_chamado()
        criar_tabelas()

        # Insere usuário e administrador de teste
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)

        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = inserir_administrador(admin_teste)

        # Cria chamado
        chamado_teste = Chamado(
            id_chamado=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )
        id_chamado_inserido = inserir_chamado(chamado_teste)

        # Cria resposta inicial
        resposta_teste = RespostaChamado(
            id_resposta_chamado=None,
            id_chamado=id_chamado_inserido,
            titulo="Resposta Original",
            descricao="Descrição Original",
            data=date(2025, 6, 30)
        )
        id_resposta_inserida = inserir_resposta(resposta_teste)

        # Atualiza resposta
        resposta_atualizada = RespostaChamado(
            id_resposta_chamado=id_resposta_inserida,
            id_chamado=id_chamado_inserido,
            titulo="Resposta Atualizada",
            descricao="Descrição Atualizada",
            data=date(2025, 7, 1)
        )

        # Act
        resultado = atualizar_resposta(resposta_atualizada)

        # Assert
        assert resultado == True, "A atualização da resposta deveria retornar True"
        resposta_db = obter_resposta_por_id(id_resposta_inserida)
        assert resposta_db.titulo == "Resposta Atualizada", "O título da resposta atualizada não confere"
        assert resposta_db.descricao == "Descrição Atualizada", "A descrição da resposta atualizada não confere"
        assert str(resposta_db.data) == "2025-07-01", "A data da resposta atualizada não confere"

    def test_excluir_resposta(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela_chamado()
        criar_tabelas()

        # Insere usuário e administrador de teste
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)

        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = inserir_administrador(admin_teste)

        # Cria chamado
        chamado_teste = Chamado(
            id_chamado=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )
        id_chamado_inserido = inserir_chamado(chamado_teste)

        # Insere resposta
        resposta_teste = RespostaChamado(
            id_resposta_chamado=None,
            id_chamado=id_chamado_inserido,
            titulo="Resposta para exclusão",
            descricao="Esta resposta será excluída",
            data=date(2025, 6, 30)
        )
        id_resposta = inserir_resposta(resposta_teste)

        # Act
        resultado = excluir_resposta(id_resposta)

        # Assert
        assert resultado == True, "A exclusão da resposta deveria retornar True"
        resposta_db = obter_resposta_por_id(id_resposta)
        assert resposta_db is None, "A resposta deveria ter sido excluída"

    def test_obter_todas_respostas_paginado(self, test_db):
        # Arrange: cria tabelas necessárias
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela_chamado()
        criar_tabelas()

        # Insere usuário e administrador de teste
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)

        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = inserir_administrador(admin_teste)

        # Cria chamado
        chamado_teste = Chamado(
            id_chamado=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )
        id_chamado_inserido = inserir_chamado(chamado_teste)

        # Cria duas respostas válidas
        resposta1 = RespostaChamado(
            id_resposta_chamado=None,
            id_chamado=id_chamado_inserido,
            titulo="Resposta 1",
            descricao="Descrição 1",
            data=date(2025, 6, 30)
        )
        resposta2 = RespostaChamado(
            id_resposta_chamado=None,
            id_chamado=id_chamado_inserido,
            titulo="Resposta 2",
            descricao="Descrição 2",
            data=date(2025, 7, 1)
        )

        inserir_resposta(resposta1)
        inserir_resposta(resposta2)

        # Act
        respostas = obter_todas_respostas_paginado(5, 0)

        # Assert
        assert len(respostas) == 2, "Deveria retornar duas respostas"
        # Note: a consulta ordena por data DESC, então resposta2 vem primeiro
        assert respostas[0].titulo == "Resposta 2", "O título da primeira resposta não confere"
        assert respostas[1].titulo == "Resposta 1", "O título da segunda resposta não confere"

    def test_obter_resposta_por_id(self, test_db):
        # Arrange
        # Criar todas as tabelas necessárias
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela_chamado()
        criar_tabelas()

        # Inserir o usuário
        usuario = Usuario(
            id_usuario=0,
            nome="Usuario Teste",
            email="usuario@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        id_usuario = inserir_usuario(usuario)

        # Inserir o administrador
        admin = Administrador(
            id_admin=0,
            nome="Admin Teste",
            email="admin@teste.com",
            senha="12345678"
        )
        id_admin = inserir_administrador(admin)

        # Criar o chamado referenciando os IDs válidos
        chamado_teste = Chamado(
            id_chamado=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Chamado Teste",
            descricao="Descrição Teste",
            status="aberto",
            data="2025-06-30"
        )
        id_chamado_inserido = inserir_chamado(chamado_teste)

        # Criar a resposta referenciando o ID do chamado válido
        resposta_teste = RespostaChamado(
            id_resposta_chamado=None,
            id_chamado=id_chamado_inserido,
            titulo="Resposta Teste",
            descricao="Descrição da Resposta Teste",
            data=date(2025, 6, 30)
        )
        id_resposta_inserida = inserir_resposta(resposta_teste)

        # Act
        resposta_db = obter_resposta_por_id(id_resposta_inserida)

        # Assert
        assert resposta_db is not None
        assert resposta_db.id_resposta_chamado == id_resposta_inserida
        assert resposta_db.id_chamado == id_chamado_inserido
        assert resposta_db.titulo == resposta_teste.titulo
        assert resposta_db.descricao == resposta_teste.descricao
        assert str(resposta_db.data) == "2025-06-30"
