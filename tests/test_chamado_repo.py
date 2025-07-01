import os
import sys

from data.administrador_model import *
from data.administrador_repo import *
from data.chamado_model import Chamado
from data.chamado_repo import *
from data.usuario_model import Usuario
from data.usuario_repo import *
from data.usuario_sql import *

class TestChamadoRepo:
    def test_criar_tabelas(self, test_db):
        #Arrange
        # Act
        resultado = criar_tabelas()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_chamado(self, test_db):
        # Arrange
        criar_tabelas()

        # Inserindo usuário e admin válidos
        usuario = Usuario(0, "Usuário Teste", "usuario@email.com", "12345678", "99999999999")
        id_usuario = inserir_usuario(usuario)

        admin = Administrador(0, "Admin Teste", "admin@email.com", "12345678")
        id_admin = inserir_administrador(admin)

        # Criando chamado com IDs válidos
        chamado_teste = Chamado(0, id_usuario, id_admin, "Título Chamado", "Descrição", "Status", "Data")

        # Act
        id_chamado_criado = inserir_chamado(chamado_teste)

        # Assert
        chamado_db = obter_chamado_por_id(id_chamado_criado)
        assert chamado_db is not None, "O chamado retornado não deveria ser None"
        assert chamado_db.id_usuario == id_usuario, "O ID do usuário não confere"
        assert chamado_db.id_admin == id_admin, "O ID do administrador não confere"
        assert chamado_db.titulo == "Título Chamado", "O título do chamado não confere"
        assert chamado_db.descricao == "Descrição", "A descrição do chamado não confere"
        assert chamado_db.status == "Status", "O status do chamado não confere"
        assert chamado_db.data == "Data", "A data do chamado não confere"

    def test_inserir_chamado(self, test_db):
        # Arrange
        criar_tabelas()
        chamado_teste = Chamado(0, 0, 0, "Título Chamado", "Descrição", "Status", "Data")
        # Act
        id_chamado_inserido = inserir_chamado(chamado_teste)
         # Assert
        chamado_db = obter_chamado_por_id(id_chamado_inserido)
        assert chamado_db is not None, "A chamado inserido não deveria ser None"
        assert chamado_db.id_usuario == 1, "O id do usuário inserido não confere"
        assert chamado_db.id_admin == 2,"O id do administrador inserido não confere"
        assert chamado_db.titulo == "Título Chamado", "O título do chamado inserido não confere"
        assert chamado_db.descricao == "Descrição", "A descrição do chamado inserido não confere"
        assert chamado_db.status == "Status", "O status do chamado inserido não confere"
        assert chamado_db.data == "Data", "A data do chamado inserido não confere"

    def test_atualizar_status_chamado(self, test_db):
        # Arrange
        criar_tabelas()
        chamado_teste = Chamado(0, 0, 0, "Título Chamado", "Descrição", "aberto", "Data")
        id_chamado_inserido = inserir_chamado(chamado_teste)

        # Act
        resultado = atualizar_status_chamado(id_chamado_inserido, "resolvido")

        # Assert
        assert resultado == True, "A atualização do status deveria retornar True"
        chamado_db = obter_chamado_por_id(id_chamado_inserido)
        assert chamado_db.status == "resolvido", "O status do chamado atualizado não confere"


    def test_atualizar_status_chamado(self, test_db):
        # Arrange
        criar_tabelas()
        criar_tabela_administrador()
        criar_tabela_usuario()

        with get_connection() as conn:
            cursor = conn.cursor()

            # Inserir usuário
            cursor.execute(
                "INSERT INTO usuario (nome, email, senha, telefone) VALUES (?, ?, ?, ?)",
                ("Usuário Teste", "usuario@email.com", "12345678", "99999999999")
            )
            id_usuario = cursor.lastrowid

            # Inserir admin
            cursor.execute(
                "INSERT INTO administrador (nome, email, senha) VALUES (?, ?, ?)",
                ("Admin Teste", "admin@email.com", "12345678")
            )
            id_admin = cursor.lastrowid

            # Inserir chamado com status 'aberto'
            cursor.execute(
                "INSERT INTO chamado (id_usuario, id_admin, titulo, descricao, status, data) VALUES (?, ?, ?, ?, ?, ?)",
                (id_usuario, id_admin, "Título Chamado", "Descrição", "aberto", "2025-06-30")
            )
            id_chamado_inserido = cursor.lastrowid

        # Act
        resultado = atualizar_status_chamado(id_chamado_inserido, "resolvido")

        # Assert
        assert resultado == True, "A atualização do status deveria retornar True"
        chamado_db = obter_chamado_por_id(id_chamado_inserido)
        assert chamado_db.status == "resolvido", "O status do chamado atualizado não confere"



    def test_excluir_chamado(self, test_db, chamado_exemplo):
        # Arrange
        criar_tabelas()        
        id_chamado_inserido = inserir_chamado(chamado_exemplo)
        # Act
        resultado = excluir_chamado(id_chamado_inserido)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        chamado_excluido = obter_chamado_por_id(id_chamado_inserido)
        assert chamado_excluido == None, "O chamado excluído deveria ser None"
        chamado_excluido = obter_chamado_por_id(id_chamado_inserido)
        assert chamado_excluido is None, "o chamado excluído deveria ser None"


    