import os
import sys
from data.veterinario_repo import *
from data.veterinario_model import Veterinario
from data.usuario_model import Usuario
from data.usuario_repo import *

class TestVeterinarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_veterinario()
        # Assert
        assert resultado == True, "A criação da tabela de veterinários deveria retornar True"

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
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste"
        )
        # Insere um usuário para a FK id_usuario        
        id_novo_veterinario = inserir_veterinario(novo_veterinario)
        # Act
        # Assert
        assert id_novo_veterinario is not None, "A inserção do veterinário deveria retornar um ID válido"
        veterinario_db = obter_por_id(id_novo_veterinario)
        assert veterinario_db is not None, "O veterinário inserido não deveria ser None"
        assert veterinario_db.id_usuario == id_novo_veterinario, "O ID do veterinário inserido não confere"
        assert veterinario_db.nome == "Veterinario Teste", "O nome do veterinário inserido não confere"
        assert veterinario_db.email == "vet@gmail.com", "O email do veterinário inserido não confere"
        assert veterinario_db.senha == "senha123", "A senha do veterinário inserido não confere"
        assert veterinario_db.telefone == "11999999999", "O telefone do veterinário inserido não confere"
        assert veterinario_db.crmv == "SP-123456", "O CRMV do veterinário inserido não confere"
        assert veterinario_db.verificado == False, "O status de verificado do veterinário inserido não confere"
        assert veterinario_db.bio == "Veterinário para teste", "A bio do veterinário inserido não confere"    

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
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste"
        )        
        id_novo_veterinario = inserir_veterinario(novo_veterinario)
        veterinario_inserido = obter_por_id(id_novo_veterinario)
        
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
        assert resultado == True, "A atualização do veterinário deveria retornar True"
        veterinario_db = obter_por_id(id_novo_veterinario)
        assert veterinario_db.nome == "Dr. Atualizado", "O nome do veterinário não foi atualizado corretamente"
        assert veterinario_db.email == "atualizado@example.com", "O email do veterinário não foi atualizado corretamente"
        assert veterinario_db.telefone == "11988888888", "O telefone do veterinário não foi atualizado corretamente"
        assert veterinario_db.crmv == "SP-654321", "O CRMV do veterinário não foi atualizado corretamente"
        assert veterinario_db.verificado == True, "O status de verificado não foi atualizado corretamente"
        assert veterinario_db.bio == "Bio atualizada", "A bio do veterinário não foi atualizada corretamente"

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
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste"
        )
        id_novo_veterinario = inserir_veterinario(novo_veterinario)
        #act
        resultado = excluir_veterinario(id_novo_veterinario)
        # Assert
        assert resultado == True, "A exclusão do veterinário deveria retornar True" 
        veterinario_excluido = obter_por_id(id_novo_veterinario)
        assert veterinario_excluido is None, "O veterinário excluído deveria ser None"

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
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste"
        )     
        vet2 = Veterinario(
            id_usuario=1,
            nome="Dr. B",
            email="b@example.com",
            senha="senhaB",
            telefone="22222222222",
            crmv="CRMV-B",
            verificado=True,
            bio="Veterinário B"
        )
        inserir_veterinario(vet1)
        inserir_veterinario(vet2)
        
        # Act
        veterinarios_db = obter_por_pagina(2, 0)    
        # Assert
        assert len(veterinarios_db) == 2, "Deveriam ser obtidos 2 veterinários"
        assert veterinarios_db[0].nome == "Veterinario Teste", "O nome do primeiro veterinário obtido não confere"
        assert veterinarios_db[1].nome == "Dr. B", "O nome do segundo veterinário obtido não confere"
        
        
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
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste"
        )
        inserir_veterinario(veterinario_teste)
        # Act
        veterinario_db = obter_por_id(1)
        # Assert
        assert veterinario_db is not None, "O veterinário obtido não deveria ser None"
        assert veterinario_db.id_usuario == veterinario_teste.id_usuario, "O ID do veterinário obtido não confere"
        assert veterinario_db.nome == "Dr. Teste", "O nome do veterinário obtido não confere"
        assert veterinario_db.crmv == "SP-123456", "O CRMV do veterinário obtido não confere"
        assert veterinario_db.bio == "Veterinário para teste", "A bio do veterinário obtido não confere"
        