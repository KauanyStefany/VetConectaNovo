from data.tutor_model import Tutor
from data.tutor_repo import *
from data.usuario_repo import *
from data.usuario_model import Usuario


class TestTutorRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        criar_tabela_usuario()  # Precisa criar a tabela usuario primeiro
        # Act
        resultado = criar_tabela_tutor()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_tutor(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        
        # Criar tutor (o repositório vai inserir o usuário automaticamente)
        tutor_teste = Tutor(0, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        
        # Act
        id_tutor_inserido = inserir_tutor(tutor_teste)
        
        # Assert
        assert id_tutor_inserido is not None, "O ID do tutor inserido não deveria ser None"
        tutor_obtido = obter_tutor_por_id(id_tutor_inserido)
        assert tutor_obtido is not None, "O tutor inserido não deveria ser None"
        assert tutor_obtido.id_usuario == id_tutor_inserido, f"O tutor inserido deveria ter ID igual a {id_tutor_inserido}"
        assert tutor_obtido.nome == "Tutor Teste", "O nome do tutor inserido não confere"
        assert tutor_obtido.email == "tutor@gmail.com", "O email do tutor inserido não confere"
        assert tutor_obtido.telefone == "123456789", "O telefone do tutor inserido não confere"

    def test_atualizar_tutor(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        
        # Inserir tutor (repositório insere usuário automaticamente)
        tutor_exemplo = Tutor(0, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_exemplo)
        tutor_inserido = obter_tutor_por_id(id_tutor_inserido)
        
        # Act
        tutor_inserido.nome = "Tutor Atualizado"
        tutor_inserido.email = "email_atualizado@gmail.com"
        tutor_inserido.telefone = "987654321"
        resultado = atualizar_tutor(tutor_inserido)
        
        # Assert
        assert resultado == True, "A atualização do tutor deveria retornar True"
        tutor_obtido = obter_tutor_por_id(id_tutor_inserido)
        assert tutor_obtido.nome == "Tutor Atualizado", "O nome do tutor atualizado não confere"
        assert tutor_obtido.email == "email_atualizado@gmail.com", "O email do tutor atualizado não confere"
        assert tutor_obtido.telefone == "987654321", "O telefone do tutor atualizado não confere"
    
    def test_atualizar_senha(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        
        # Inserir tutor (repositório insere usuário automaticamente)
        tutor_exemplo = Tutor(0, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_exemplo)
        
        # Act
        nova_senha = "87654321"
        resultado = atualizar_senha_usuario(id_tutor_inserido, nova_senha)
        
        # Assert
        assert resultado == True, "A atualização da senha deveria retornar True"
        # Verificar através do usuário, pois senha está na tabela usuario
        usuario_db = obter_usuario_por_id(id_tutor_inserido)
        assert usuario_db.senha == nova_senha, "A senha do tutor atualizado não confere"

    def test_excluir_tutor(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        
        # Inserir tutor (repositório insere usuário automaticamente)
        tutor_exemplo = Tutor(0, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_exemplo)
        
        # Act
        resultado = excluir_tutor(id_tutor_inserido)
        
        # Assert
        assert resultado == True, "A exclusão do tutor deveria retornar True"
        tutor_excluido = obter_tutor_por_id(id_tutor_inserido)
        assert tutor_excluido == None, "O tutor excluído deveria ser None"

    def test_obter_todos_tutores(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        
        # Inserir tutores (repositório insere usuários automaticamente)
        tutor1 = Tutor(0, "Tutor 1", "tutor1@gmail.com", "12345678", "123456789")
        tutor2 = Tutor(0, "Tutor 2", "tutor2@gmail.com", "87654321", "987654321")
        inserir_tutor(tutor1)
        inserir_tutor(tutor2)
        
        # Act
        tutores = obter_todos_tutores_paginado(10, 0)  # Passar limite e offset
        
        # Assert
        assert len(tutores) == 2, "Deveria retornar dois tutores"
        assert tutores[0].nome == "Tutor 1", "O nome do primeiro tutor não confere"
        assert tutores[1].nome == "Tutor 2", "O nome do segundo tutor não confere"
    
    def test_obter_tutor_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        
        # Inserir tutor (repositório insere usuário automaticamente)
        tutor_teste = Tutor(0, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_teste)
        
        # Act
        tutor_obtido = obter_tutor_por_id(id_tutor_inserido)
        
        # Assert
        assert tutor_obtido is not None, "O tutor obtido não deveria ser None"
        assert tutor_obtido.nome == "Tutor Teste", "O nome do tutor não confere"
        assert tutor_obtido.email == "tutor@gmail.com", "O email do tutor não confere"
        assert tutor_obtido.telefone == "123456789", "O telefone do tutor não confere"