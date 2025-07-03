import os
import sys
from data.administrador_repo import criar_tabela_administrador, inserir_administrador
from data.administrador_model import Administrador
from data.verificacao_crmv_model import VerificacaoCRMV
from data.verificacao_crmv_repo import *
from data.veterinario_repo import criar_tabela_veterinario, inserir_veterinario   
from data.veterinario_model import Veterinario
from data.usuario_repo import criar_tabela_usuario

class TestVerificacaoCRMVRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela de verificações de CRMV deveria retornar True"
        
    def test_inserir_verificacao(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        
        # Insere um veterinário para a FK id_veterinario
        veterinario = Veterinario(
            id_usuario=0, nome="Veterinário Teste", email="email123@gmail.com", 
            senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""
        )
        veterinario_id = inserir_veterinario(veterinario) 
        
        # Insere um administrador para a FK id_admin
        admin = Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        )
        admin_id = inserir_administrador(admin)
        
        # Cria uma verificação de CRMV
        verificacao = VerificacaoCRMV(
            id=0,
            veterinario=Veterinario(id_usuario=veterinario_id, nome="Veterinário Teste", email="email123@gmail.com", 
            senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""),
            administrador=Administrador(id_admin=admin_id, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"),
            data_verificacao="2025-06-30",
            status_verificacao="pendente"
        )
        
        # Act
        resultado = inserir(verificacao)
        
        # Assert
        assert resultado is not None, "A inserção da verificação de CRMV deveria retornar um ID"
        verificacao_db = obter_por_id(resultado)
        assert verificacao_db is not None, "A verificação de CRMV inserida não deveria ser None"
        assert verificacao_db.veterinario.id_usuario == veterinario_id, "O ID do veterinário da verificação inserida não confere"
        assert verificacao_db.administrador.id_admin == admin_id, "O ID do administrador da verificação inserida não confere"
        assert verificacao_db.status_verificacao == "pendente", "O status da verificação inserida não confere"
        
    def test_atualizar_verificacao(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        
        veterinario = Veterinario(
            id_usuario=0, nome="Veterinário Teste", email="email123@gmail.com", 
            senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""
        )
        veterinario_id = inserir_veterinario(veterinario)
        
        admin = Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        )
        admin_id = inserir_administrador(admin)
        
        verificacao = VerificacaoCRMV(
            id=0,
            veterinario=Veterinario(id_usuario=veterinario_id, nome="Veterinário Teste", email="email123@gmail.com", 
                                  senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""),
            administrador=Administrador(id_admin=admin_id, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"),
            data_verificacao="2025-06-30",
            status_verificacao="pendente"
        )
        inserir(verificacao)
        
        # Act
        resultado = atualizar(veterinario_id, "verificado", admin_id)
        
        # Assert
        assert resultado == True, "A atualização da verificação de CRMV deveria retornar True"
        
    def test_excluir_verificacao(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        
        veterinario = Veterinario(
            id_usuario=0, nome="Veterinário Teste", email="email123@gmail.com", 
            senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""
        )
        veterinario_id = inserir_veterinario(veterinario)
        
        admin = Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        )
        admin_id = inserir_administrador(admin)
        
        verificacao = VerificacaoCRMV(
            id=0,
            veterinario=Veterinario(id_usuario=veterinario_id, nome="Veterinário Teste", email="email123@gmail.com", 
                                  senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""),
            administrador=Administrador(id_admin=admin_id, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"),
            data_verificacao="2025-06-30",
            status_verificacao="pendente"
        )
        inserir(verificacao)
        
        # Act
        resultado = excluir(veterinario_id)
        
        # Assert
        assert resultado == True, "A exclusão da verificação de CRMV deveria retornar True"
    
    def test_obter_todos_paginado(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        
        veterinario = Veterinario(
            id_usuario=0, nome="Veterinário Teste", email="email123@gmail.com", 
            senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""
        )
        veterinario_id = inserir_veterinario(veterinario)
        
        admin = Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        )
        admin_id = inserir_administrador(admin)
        
        verificacao = VerificacaoCRMV(
            id=0,
            veterinario=Veterinario(id_usuario=veterinario_id, nome="Veterinário Teste", email="email123@gmail.com", 
                                  senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""),
            administrador=Administrador(id_admin=admin_id, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"),
            data_verificacao="2025-06-30",
            status_verificacao="pendente"
        )
        inserir(verificacao)
        
        # Act
        resultado = obter_todos_paginado(10, 0)
        
        # Assert
        assert resultado is not None, "A consulta de verificações de CRMV deveria retornar resultados"
        assert len(resultado) > 0, "A consulta de verificações de CRMV deveria retornar mais de 0 resultados"
        assert resultado[0].veterinario.id_usuario == veterinario_id, "O ID do veterinário na verificação retornada não confere"
        assert resultado[0].administrador.id_admin == admin_id, "O ID do administrador na verificação retornada não confere"
        assert resultado[0].status_verificacao == "pendente", "O status da verificação retornada não confere"
        
    def test_obter_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        
        veterinario = Veterinario(
            id_usuario=0, nome="Veterinário Teste", email="email123@gmail.com", 
            senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""
        )
        veterinario_id = inserir_veterinario(veterinario)
        
        admin = Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        )
        admin_id = inserir_administrador(admin)
        
        verificacao = VerificacaoCRMV(
            id=0,
            veterinario=Veterinario(id_usuario=veterinario_id, nome="Veterinário Teste", email="email123@gmail.com", senha="senha123", telefone="12345678900", crmv="CRMV123", verificado=False, bio=""),
            administrador=Administrador(id_admin=admin_id, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"),
            data_verificacao="2025-06-30",
            status_verificacao="pendente"
        )
        verificacao_id = inserir(verificacao)
        
        # Act
        resultado = obter_por_id(verificacao_id)
        
        # Assert
        assert resultado is not None, "A consulta de verificação de CRMV deveria retornar um resultado"
        assert resultado.id == verificacao_id, "O ID da verificação retornada não confere"
        assert resultado.veterinario.id_usuario == veterinario_id, "O ID do veterinário na verificação retornada não confere"
        assert resultado.administrador.id_admin == admin_id, "O ID do administrador na verificação retornada não confere"
        assert resultado.status_verificacao == "pendente", "O status da verificação retornada não confere"