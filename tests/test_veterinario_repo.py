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
        resultado = criar_tabela_tutor()
        # Assert
        assert resultado == True, "A criação da tabela de veterinários deveria retornar True"


    def test_inserir_veterinario(self, test_db):
        # Arrange
        criar_tabela_tutor()  # Cria a tabela veterinário
        criar_tabela_usuario() # Certifique que a tabela usuário existe
        
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(
            id_usuario=0,
            nome="Veterinario Teste",
            email="vet@teste.com",
            senha="senha123",
            telefone="11999999999"
        ))
        
        # Cria um veterinário associado a esse usuário
        veterinario_teste = Veterinario(
            id_usuario=usuario_id,        # FK para usuario
            id_veterinario=usuario_id,    # Geralmente igual ao id_usuario, pelo que vi no JOIN
            nome="Veterinario Teste",
            email="vet@teste.com",
            senha="senha123",
            telefone="11999999999",
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste"
        )
        
        # Act
        inserido = inserir_veterinario(veterinario_teste)
        
        # Assert
        assert inserido == True, "A inserção do veterinário deveria retornar True"
        veterinario_db = obter_por_id(usuario_id)
        assert veterinario_db is not None, "O veterinário inserido não deveria ser None"
        assert veterinario_db.id_veterinario == usuario_id, "O ID do veterinário inserido não confere"
        assert veterinario_db.nome == "Veterinario Teste", "O nome do veterinário inserido não confere"
        assert veterinario_db.crmv == "SP-123456", "O CRMV do veterinário inserido não confere"
        assert veterinario_db.bio == "Veterinário para teste", "A bio do veterinário inserido não confere"


    def test_atualizar_veterinario(self, test_db):
        # Arrange
        criar_tabela_tutor()
        veterinario_teste = Veterinario(
            id_veterinario=1,
            nome="Dr. Original",
            email="original@example.com",
            senha="senha123",
            telefone="11999999999",
            crmv="SP-12345",
            verificado=False,
            bio="Bio original"
        )
        inserir_veterinario(veterinario_teste)
        veterinario_inserido = obter_por_id(veterinario_teste.id_veterinario)

        # Act
        veterinario_inserido.bio = "Bio atualizada"
        veterinario_inserido.verificado = True
        veterinario_inserido.nome = "Dr. Atualizado"
        veterinario_inserido.email = "atualizado@example.com"
        veterinario_inserido.senha = "novasenha"
        
        resultado = atualizar_veterinario(veterinario_inserido)

        # Assert
        assert resultado == True, "A atualização do veterinário deveria retornar True"
        veterinario_db = obter_por_id(veterinario_teste.id_veterinario)
        assert veterinario_db.bio == "Bio atualizada", "A bio do veterinário não foi atualizada corretamente"
        assert veterinario_db.verificado == True, "O status de verificado não foi atualizado corretamente"
        assert veterinario_db.nome == "Dr. Atualizado", "O nome do veterinário não foi atualizado corretamente"
        assert veterinario_db.email == "atualizado@example.com", "O email do veterinário não foi atualizado corretamente"

    def test_excluir_veterinario(self, test_db):
        # Arrange
        criar_tabela_tutor()
        veterinario_teste = Veterinario(
            id_usuario=1,
            id_veterinario=1,
            nome="Dr. Remover",
            email="remover@example.com",
            senha="senha123",
            telefone="11999999999",
            crmv="SP-54321",
            verificado=False,
            bio="Será removido"
        )
        inserir_veterinario(veterinario_teste)
        
        # Act
        resultado = excluir_veterinario(veterinario_teste.id_veterinario)
        
        # Assert
        assert resultado == True, "A exclusão do veterinário deveria retornar True"
        veterinario_excluido = obter_por_id(veterinario_teste.id_veterinario)
        assert veterinario_excluido is None, "O veterinário excluído deveria ser None"

    def test_obter_todos_veterinarios(self, test_db):
        # Arrange
        criar_tabela_tutor()
        vet1 = Veterinario(
            id_usuario=1,
            id_veterinario=1,
            nome="Dr. A",
            email="a@example.com",
            senha="senhaA",
            telefone="11111111111",
            crmv="CRMV-A",
            verificado=False,
            bio="Veterinário A"
        )
        vet2 = Veterinario(
            id_usuario=2,
            id_veterinario=2,
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
        veterinarios = obter_todos()
        
        # Assert
        assert len(veterinarios) >= 2, "Deveria retornar pelo menos dois veterinários"
        nomes = [v.nome for v in veterinarios]
        assert "Dr. A" in nomes, "O nome 'Dr. A' deveria estar na lista de veterinários"
        assert "Dr. B" in nomes, "O nome 'Dr. B' deveria estar na lista de veterinários"
