import os
import sys
from data.administrador_repo import criar_tabela_administrador, inserir_administrador
from data.verificacao_crmv_model import VerificacaoCRMV
from data.verificacao_crmv_repo import *
from data.veterinario_repo import criar_tabela_veterinario, inserir_veterinario
class TestVerificacaoCRMVRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela de verificações de CRMV deveria retornar True"
        
    def test_inserir_verificacao(self, test_db):
        # Arrange
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        # Insere um veterinário para a FK id_veterinario
        veterinario_id = inserir_veterinario(Veterinario(
            id_veterinario=0, nome="Veterinário Teste", email="email123@gmail.com", senha="senha123", telefone="12345678900", crmv="CRMV123"
        )) 
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        ))
        # Cria uma verificação de CRMV
        verificacao = VerificacaoCRMV(
            id_verificacao=0,
            id_veterinario=veterinario_id,
            id_admin=admin_id,
            data_verificacao="2025-06-30",
            status="pendente"
        )
        # Act
        resultado = inserir(verificacao)
        # Assert
        assert resultado == True, "A inserção da verificação de CRMV deveria retornar True"
        verificacao_db = obter_por_id(resultado)
        assert verificacao_db is not None, "A verificação de CRMV inserida não deveria ser None"
        assert verificacao_db.id_veterinario == veterinario_id, "O ID do veterinário da verificação inserida não confere"
        assert verificacao_db.id_admin == admin_id, "O ID do administrador da verificação inserida não confere"
        assert verificacao_db.status == "pendente", "O status da verificação inserida não confere"  
    def test_atualizar_verificacao(self, test_db):
        # Arrange
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        veterinario_id = inserir_veterinario(Veterinario(
            id_veterinario=0, nome="Veterinário Teste", email="email123@gmail.com", senha="senha123", telefone="12345678900", crmv="CRMV123"
        ))
        admin_id = inserir_administrador(Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        ))
        verificacao = VerificacaoCRMV(
            id_verificacao=0,
            id_veterinario=veterinario_id,
            id_admin=admin_id,
            data_verificacao="2025-06-30",
            status="pendente"
        )
        inserir(verificacao)
        # Act
        verificacao.status = "aprovada"
        resultado = atualizar(verificacao)
        # Assert
        assert resultado == True, "A atualização da verificação de CRMV deveria retornar True"
        verificacao_db = obter_por_id(verificacao.id_verificacao)
        assert verificacao_db is not None, "A verificação de CRMV atualizada não deveria ser None"
        assert verificacao_db.status == "aprovada", "O status da verificação atualizada não confere"
        
    def test_excluir_verificacao(self, test_db):
        # Arrange
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        veterinario_id = inserir_veterinario(Veterinario(
            id_veterinario=0, nome="Veterinário Teste", email="email123@gmail.com", senha="senha123", telefone="12345678900", crmv="CRMV123"
        ))
        admin_id = inserir_administrador(Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        ))
        verificacao = VerificacaoCRMV(
            id_verificacao=0,
            id_veterinario=veterinario_id,
            id_admin=admin_id,
            data_verificacao="2025-06-30",
            status="pendente"
        )
        inserir(verificacao)
        # Act
        resultado = excluir(verificacao.id_verificacao)
        # Assert
        assert resultado == True, "A exclusão da verificação de CRMV deveria retornar True"
        verificacao_db = obter_por_id(verificacao.id_verificacao)
        assert verificacao_db is None, "A verificação de CRMV excluída não deveria ser encontrada"
    
    def test_obter_todos_paginado(self, test_db):
        # Arrange
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        veterinario_id = inserir_veterinario(Veterinario(
            id_veterinario=0, nome="Veterinário Teste", email="email123@gmail.com", senha="senha123", telefone="12345678900", crmv="CRMV123"
        ))
        admin_id = inserir_administrador(Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        ))
        verificacao = VerificacaoCRMV(
            id_verificacao=0,
            id_veterinario=veterinario_id,
            id_admin=admin_id,
            data_verificacao="2025-06-30",
            status="pendente"
        )
        inserir(verificacao)
        # Act
        resultado = obter_todos_paginado(1, 10)
        # Assert
        assert resultado is not None, "A consulta de verificações de CRMV deveria retornar resultados"
        assert len(resultado) > 0, "A consulta de verificações de CRMV deveria retornar mais de 0 resultados"
        assert resultado[0].id_veterinario == veterinario_id, "O ID do veterinário na verificação retornada não confere"
        assert resultado[0].id_admin == admin_id, "O ID do administrador na verificação retornada não confere"
        assert resultado[0].status == "pendente", "O status da verificação retornada não confere"
    def test_obter_por_id(self, test_db):
        # Arrange
        criar_tabela_veterinario()
        criar_tabela_administrador()
        criar_tabela()
        veterinario_id = inserir_veterinario(Veterinario(
            id_veterinario=0, nome="Veterinário Teste", email="email123@gmail.com", senha="senha123", telefone="12345678900", crmv="CRMV123"
        ))
        admin_id = inserir_administrador(Administrador(
            id_admin=0, nome="Admin Teste", email="email12345@gmail.com", senha="senha12345"
        ))
        verificacao = VerificacaoCRMV(
            id_verificacao=0,
            id_veterinario=veterinario_id,
            id_admin=admin_id,
            data_verificacao="2025-06-30",
            status="pendente"
        )
        inserir(verificacao)
        # Act
        resultado = obter_por_id(verificacao.id_verificacao)
        # Assert
        assert resultado is not None, "A consulta de verificação de CRMV deveria retornar um resultado"
        assert resultado.id == verificacao.id_verificacao, "O ID da verificação retornada não confere"
        assert resultado.veterinario == veterinario_id, "O ID do veterinário na verificação retornada não confere"
        assert resultado.administrador == admin_id, "O ID do administrador na verificação retornada não confere"
        assert resultado.status_verificacao == "pendente", "O status da verificação retornada não confere"
        assert resultado.data_verificacao == "2025-06-30", "A data da verificação retornada não confere"
        
