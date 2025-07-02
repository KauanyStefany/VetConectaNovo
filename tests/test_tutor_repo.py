from data.tutor_model import Tutor
from data.tutor_repo import *
from data.usuario_repo import *
from data.usuario_model import Usuario



class TestTutorRepo:
    def test_criar_tabela(self, test_db):
        # Act
        resultado = criar_tabela_tutor()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_tutor(self, test_db):
        # Arrange
        criar_tabela_tutor()
        tutor_teste = Tutor(1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        
            # Act
        id_tutor_inserido = inserir_tutor(tutor_teste)
            # Assert
        tutor_obtido = obter_tutor_por_id(id_tutor_inserido)
        assert tutor_obtido is not None, "O tutor inserido não deveria ser None"
        assert tutor_obtido.id_usuario == 1, "O tutor inserido deveria ter um ID igual a 1"
        assert tutor_obtido.nome == "Tutor Teste", "O nome do tutor inserido não confere"
        assert tutor_obtido.email == "tutor@gmail.com", "O email do tutor inserido não confere"
        assert tutor_obtido.senha == "12345678", "A senha do tutor inserido não confere"
        assert tutor_obtido.telefone == "123456789", "O telefone do tutor inserido não confere"


    def test_inserir_administrador(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(0, "Admin Teste", "admin@gmail.com", "12345678")
            # Act
        id_admin_inserido = inserir_administrador(admin_teste)
            # Assert
        admin_db = obter_administrador_por_id(id_admin_inserido)
        assert admin_db is not None, "O administrador inserido não deveria ser None"
        assert admin_db.id_admin == 1, "O administrador inserido deveria ter um ID igual a 1"
        assert admin_db.nome == "Admin Teste", "O nome do administrador inserido não confere"
        assert admin_db.email == "admin@gmail.com", "O email do administrador inserido não confere"
        assert admin_db.senha == "12345678", "A senha do administrador inserido não confere"



    def test_atualizar_tutor(self, test_db):
        # Arrange
        criar_tabela_tutor()
        tutor_exemplo = Tutor(1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_exemplo)
        tutor_inserido = obter_tutor_por_id(id_tutor_inserido)
        # Act
        tutor_inserido.nome = "Tutor Atualizado"
        tutor_inserido.email = "email Atualizada"
        tutor_inserido.senha = "12345678"
        tutor_inserido.telefone = "123456789"
        resultado = atualizar_tutor(tutor_obtido)
        # Assert
        assert resultado == True, "A atualização do tutor deveria retornar True"
        tutor_obtido = obter_tutor_por_id(tutor_inserido)
        assert tutor_obtido.nome == "Tutor Atualizado", "O nome do tutor atualizado não confere"
        assert tutor_obtido.email == "Email Atualizada", "O email do tutor atualizado não confere"
        assert tutor_obtido.senha == "Senha Atualizada", "A senha do tutor atualizado não confere"
        assert tutor_obtido.telefone == "Telefone Atualizado", "O telefone do tutor atualizado não confere"
    
    def test_atualizar_senha(self, test_db):
        criar_tabela_tutor
        tutor_exemplo = Tutor(1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_exemplo)
        #Act
        nova_senha ="87654321"
        resultado = atualizar_senha_usuario(id_tutor_inserido, nova_senha)
        #Assert
        assert resultado == True, "A atualização da senha deveria retornar True"
        tutor_db = obter_tutor_por_id(id_tutor_inserido)
        assert tutor_db.senha == nova_senha, "A senha do tutor atualizado não confere"

    def test_excluir_tutor(self, test_db):
        # Arrange
        tutor_exemplo = Tutor(1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_exemplo)
        # Act
        resultado = excluir_tutor(id_tutor_inserido)
        # Assert
        assert resultado == True, "A exclusão do tutor deveria retornar True"
        tutor_excluido = obter_tutor_por_id(id_tutor_inserido)
        assert tutor_excluido == None, "O tutor excluído deveria ser None"

    def test_obter_todos_tutores(self, test_db):
        # Arrange
        criar_tabela_tutor
        tutor1 = Tutor(1, "Tutor 1", "tutor1@gmail.com", "12345678", "123456789")
        tutor2 = Tutor(2, "Tutor 2", "tutor2@gmail.com", "12345678", "123456789")
        inserir_tutor(tutor1)
        inserir_tutor(tutor2)
        # Act
        tutores = obter_todos_tutores_paginado()
        # Assert
        assert len(tutores) == 2, "Deveria retornar duas categorias"
        assert tutores[0].nome == "Tutor 1", "O nome do primeiro tutor não confere"
        assert tutores[1].nome == "Tutor 2", "O nome do segundo tutor não confere"
    
    def test_obter_tutor_por_id(self, test_db):
        #Arrange
        criar_tabela_tutor()
        tutor_teste = (1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_teste)
        # Act
        tutor_obtido = obter_tutor_por_id(id_tutor_inserido)
        # Assert
        assert tutor_obtido.nome == "Tutor Atualizado", "O nome do tutor atualizado não confere"
        assert tutor_obtido.email == "Email Atualizada", "O email do tutor atualizado não confere"
        assert tutor_obtido.senha == "Senha Atualizada", "A senha do tutor atualizado não confere"
        assert tutor_obtido.telefone == "Telefone Atualizado", "O telefone do tutor atualizado não confere"        