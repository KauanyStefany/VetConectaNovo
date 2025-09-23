import os
import sys
from app.database.repositories.administrador_repo import *
from app.database.models.administrador_model import Administrador
import time

def unique_email(prefix="test"):
    """Gera um email único para testes"""
    timestamp = str(int(time.time() * 1000000))  # microsegundos
    return f"{prefix}_{timestamp}@test.com"

class TestAdministradorRepo:
    def test_criar_tabela_administrador(self, test_db):
        #Arrange
        # Act
        resultado = criar_tabela_administrador()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_administrador(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(id_admin=0, nome="Admin Teste", email=unique_email("admin"), senha="12345678")
            # Act
        id_admin_inserido = inserir_administrador(admin_teste)
            # Assert
        admin_db = obter_administrador_por_id(id_admin_inserido)
        assert admin_db is not None, "O administrador inserido não deveria ser None"
        assert admin_db.id_admin == id_admin_inserido, "O ID do administrador inserido não confere"
        assert admin_db.nome == "Admin Teste", "O nome do administrador inserido não confere"
        assert admin_db.email == admin_teste.email, "O email do administrador inserido não confere"
        assert admin_db.senha == "12345678", "A senha do administrador inserido não confere"

    def test_atualizar_administrador(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(id_admin=0, nome="Admin Teste", email=unique_email("admin"), senha="12345678")
        id_admin_inserido = inserir_administrador(admin_teste)
        admin_inserido = obter_administrador_por_id(id_admin_inserido)
            # Act
        admin_inserido.nome = "Admin Atualizado"
        admin_inserido.email = unique_email("atualizado")
        admin_inserido.senha = "12345678"
        resultado = atualizar_administrador(admin_inserido)
        # Assert
        assert resultado == True, "A atualização do administrador deveria retornar True"
        admin_db = obter_administrador_por_id(id_admin_inserido)
        assert admin_db.nome == "Admin Atualizado", "O nome do administrador atualizado não confere"
        assert admin_db.email == admin_inserido.email, "O email do administrador atualizado não confere"
        assert admin_db.senha == "12345678", "A senha do administrador atualizado não confere"

    def test_atualizar_senha(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(id_admin=0, nome="Admin Teste", email=unique_email("admin"), senha="12345678")
        id_admin_inserido = inserir_administrador(admin_teste)
        # Act
        nova_senha = "87654321"
        resultado = atualizar_senha(id_admin_inserido, nova_senha)  
        # Assert
        assert resultado == True, "A atualização da senha deveria retornar True"
        admin_db = obter_administrador_por_id(id_admin_inserido)
        assert admin_db.senha == nova_senha, "A senha do administrador atualizado não confere"



    def test_excluir_administrador(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(id_admin=0, nome="Admin Teste", email=unique_email("admin"), senha="12345678")
        id_admin_inserido = inserir_administrador(admin_teste)
        # Act
        resultado = excluir_administrador(id_admin_inserido)
        # Assert    
        assert resultado == True, "A exclusão do administrador deveria retornar True"
        admin_excluido = obter_administrador_por_id(id_admin_inserido)  
        assert admin_excluido == None, "O administrador excluído deveria ser None"


    def test_obter_todos_administradores(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin1 = Administrador(id_admin=0, nome="Admin 1", email=unique_email("admin1"), senha="12345678")
        admin2 = Administrador(id_admin=0, nome="Admin 2", email=unique_email("admin2"), senha="87654321")
        inserir_administrador(admin1)
        inserir_administrador(admin2)   
        # Act
        administradores = obter_administradores_paginado(0, 10)

        # Assert - Pode haver dados de outros testes, verificamos se pelo menos os 2 foram inseridos
        assert len(administradores) >= 2, "Deveria haver pelo menos 2 administradores"
        nomes_encontrados = [admin.nome for admin in administradores]
        assert "Admin 1" in nomes_encontrados, "Admin 1 deveria estar na lista"
        assert "Admin 2" in nomes_encontrados, "Admin 2 deveria estar na lista"

    def test_obter_administrador_por_id(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(id_admin=0, nome="Admin Teste", email=unique_email("admin"), senha="12345678")
        id_admin_inserido = inserir_administrador(admin_teste)
        # Act   
        admin_obtido = obter_administrador_por_id(id_admin_inserido)
        # Assert
        assert admin_obtido is not None, "O administrador obtido não deveria ser None"
        assert admin_obtido.id_admin == id_admin_inserido, "O ID do administrador obtido não confere"
        assert admin_obtido.nome == admin_teste.nome, "O nome do administrador obtido não confere"
        assert admin_obtido.email == admin_teste.email, "O email do administrador obtido não confere"
        assert admin_obtido.senha == admin_teste.senha, "A senha do administrador obtido não confere"

