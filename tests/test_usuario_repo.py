import os
import sys
from data.usuario_repo import *
from data.usuario_model import Usuario

class TestUsuarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_usuario()
        # Assert
        assert resultado == True, "A criação da tabela de usuários deveria retornar True"


    def test_inserir_usuario(self, test_db):
        #Arrange 
        criar_tabela_usuario()

        usuario_teste = Usuario(
            id_usuario=1, 
            nome="Usuário Teste",
            email="teste@teste.com", 
            senha="12345678", 
            telefone="12345678900"  
        )
        #Act
        id_usuario_inserido = inserir_usuario(usuario_teste)
        #Assert
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db is not None, "O usuario inserido não deveria ser None"
        assert usuario_db.id_usuario == 1, "O usuario inserido deveria ter um ID igual a 1"
        assert usuario_db.nome == "Usuário Teste", "O nome do usuario inserido não confere"
        assert usuario_db.email == "teste@teste.com", "O email do usuario não confere"
        assert usuario_db.senha == "12345678", "A senha do usuario não confere"
        assert usuario_db.telefone == "12345678900", "O telefone do usuario não confere"

    def test_atualizar_usuario(self, test_db):
        #Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(
            id_usuario=1, 
            nome="Usuário Teste",
            email="teste@teste.com", 
            senha="12345678", 
            telefone="12345678900"  
        )
        id_usuario_inserido = inserir_usuario(usuario_teste)
        usuario_inserido = obter_usuario_por_id(id_usuario_inserido)
        #Act
        usuario_inserido.nome = "Usuário Teste"
        usuario_inserido.email = "teste@teste.com"
        usuario_inserido.senha = "12345678"
        usuario_inserido.telefone = "12345678900"
        resultado = atualizar_usuario(usuario_inserido)
        #Assert
        assert resultado == True, "A atualização da categoria deveria retornar True"
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.nome == "Usuário Teste", "O nome do usuario inserido não confere"
        assert usuario_db.email == "teste@teste.com", "O email do usuario não confere"
        assert usuario_db.senha == "12345678", "A senha do usuario não confere"
        assert usuario_db.telefone == "12345678900", "O telefone do usuario não confere"


    def test_atualizar_senha_usuario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(0, "Teste", "teste@email.com", "senha_antiga", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)
        
        # Act
        nova_senha = "senha_nova123"
        resultado = atualizar_senha_usuario(id_usuario, nova_senha)
        
        # Assert
        assert resultado is True, "A atualização da senha deveria retornar True"
        usuario_atualizado = obter_usuario_por_id(id_usuario)
        assert usuario_atualizado.senha == nova_senha, "A senha do usuário não foi atualizada corretamente"

    def test_excluir_usuario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(1, "Teste", "teste@email.com", "senha123", "11999999999")
        id_usuario_inserido = inserir_usuario(usuario_teste)
        # Act
        resultado = excluir_usuario(id_usuario_inserido)
        # Assert
        assert resultado == True, "A exclusão do usuário deveria retornar True"
        usuario_excluido = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_excluido == None, "O usuário excluído deveria ser None"
    
    def test_obter_todos_usuarios_paginado(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario1 = Usuario(0, "Usuário 1", "u1@email.com", "senha1", "1111111111")
        usuario2 = Usuario(0, "Usuário 2", "u2@email.com", "senha2", "2222222222")
        inserir_usuario(usuario1)
        inserir_usuario(usuario2)

        # Act
        usuarios = obter_todos_usuarios_paginado(limite=10, offset=0)

        # Assert
        assert len(usuarios) == 2, "Deveria retornar dois usuários"
        assert usuarios[0].nome == "Usuário 1", "O nome do primeiro usuário não confere"
        assert usuarios[1].nome == "Usuário 2", "O nome do segundo usuário não confere"


    def test_obter_usuario_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario = Usuario(0, "Teste", "teste@email.com", "senha123", "11999999999")
        id_usuario = inserir_usuario(usuario)

        # Act
        usuario_db = obter_usuario_por_id(id_usuario)

        # Assert
        assert usuario_db is not None, "O usuário obtido não deveria ser None"
        assert usuario_db.id == id_usuario, "O ID do usuário obtido não confere"
        assert usuario_db.nome == usuario.nome, "O nome do usuário obtido não confere"

        