import pytest
from repo.usuario_repo import *
from model.usuario_model import Usuario


class TestUsuarioRepo:
    """Testes para o repositório de usuários"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """Setup executado antes de cada teste"""
        criar_tabela_usuario()
        
    def test_criar_tabela(self, test_db):
        """Testa a criação da tabela de usuários"""
        # Arrange - já feito no setup
        # Act
        resultado = criar_tabela_usuario()
        
        # Assert
        assert resultado == True, "A criação da tabela de usuários deveria retornar True"

    def test_inserir_usuario_sucesso(self, test_db):
        """Testa inserção de usuário com sucesso"""
        # Arrange
        usuario_teste = Usuario(
            id_usuario=0,  # 0 para auto-increment
            nome="João Silva",
            email="joao.silva@email.com",
            senha="senha123",
            telefone="11999998888"
        )
        
        # Act
        id_inserido = inserir_usuario(usuario_teste)
        
        # Assert
        assert id_inserido is not None, "ID do usuário inserido não deveria ser None"
        assert id_inserido > 0, "ID deveria ser maior que zero"
        
        # Verificar se foi salvo corretamente
        usuario_db = obter_usuario_por_id(id_inserido)
        assert usuario_db is not None, "Usuário deveria existir no banco"
        assert usuario_db.nome == usuario_teste.nome
        assert usuario_db.email == usuario_teste.email
        assert usuario_db.senha == usuario_teste.senha
        assert usuario_db.telefone == usuario_teste.telefone

    def test_inserir_usuario_email_duplicado(self, test_db):
        """Testa inserção de usuário com email duplicado"""
        # Arrange
        usuario1 = Usuario(0, "João", "email@test.com", "senha123", "11999998888")
        usuario2 = Usuario(0, "Maria", "email@test.com", "senha456", "11888887777")
        
        # Act
        inserir_usuario(usuario1)
        
        # Assert - deve falhar por email único
        with pytest.raises(Exception):
            inserir_usuario(usuario2)

    def test_atualizar_usuario_sucesso(self, test_db):
        """Testa atualização de usuário com sucesso"""
        # Arrange
        usuario_original = Usuario(0, "Nome Original", "original@email.com", "senha123", "11999998888")
        id_usuario = inserir_usuario(usuario_original)
        
        # Act
        usuario_atualizado = Usuario(
            id_usuario=id_usuario,
            nome="Nome Atualizado",
            email="atualizado@email.com",
            senha="senha123",  # senha não é atualizada por atualizar_usuario
            telefone="11777776666"
        )
        resultado = atualizar_usuario(usuario_atualizado)
        
        # Assert
        assert resultado == True, "Atualização deveria retornar True"
        
        usuario_db = obter_usuario_por_id(id_usuario)
        assert usuario_db.nome == "Nome Atualizado"
        assert usuario_db.email == "atualizado@email.com"
        assert usuario_db.telefone == "11777776666"
        assert usuario_db.senha == "senha123"  # senha não deve mudar

    def test_atualizar_usuario_inexistente(self, test_db):
        """Testa atualização de usuário inexistente"""
        # Arrange
        usuario_inexistente = Usuario(9999, "Não Existe", "nao@existe.com", "senha", "11999998888")
        
        # Act
        resultado = atualizar_usuario(usuario_inexistente)
        
        # Assert
        assert resultado == False, "Atualização de usuário inexistente deveria retornar False"

    def test_atualizar_senha_usuario_sucesso(self, test_db):
        """Testa atualização de senha com sucesso"""
        # Arrange
        usuario = Usuario(0, "João", "joao@email.com", "senha_antiga", "11999998888")
        id_usuario = inserir_usuario(usuario)
        nova_senha = "senha_nova_123"
        
        # Act
        resultado = atualizar_senha_usuario(id_usuario, nova_senha)
        
        # Assert
        assert resultado == True, "Atualização de senha deveria retornar True"
        
        usuario_db = obter_usuario_por_id(id_usuario)
        assert usuario_db.senha == nova_senha, "Senha deveria ter sido atualizada"

    def test_atualizar_senha_usuario_inexistente(self, test_db):
        """Testa atualização de senha de usuário inexistente"""
        # Arrange
        id_inexistente = 9999
        nova_senha = "senha_nova"
        
        # Act
        resultado = atualizar_senha_usuario(id_inexistente, nova_senha)
        
        # Assert
        assert resultado == False, "Atualização de senha de usuário inexistente deveria retornar False"

    def test_excluir_usuario_sucesso(self, test_db):
        """Testa exclusão de usuário com sucesso"""
        # Arrange
        usuario = Usuario(0, "João", "joao@email.com", "senha123", "11999998888")
        id_usuario = inserir_usuario(usuario)
        
        # Act
        resultado = excluir_usuario(id_usuario)
        
        # Assert
        assert resultado == True, "Exclusão deveria retornar True"
        
        usuario_db = obter_usuario_por_id(id_usuario)
        assert usuario_db is None, "Usuário não deveria mais existir"

    def test_excluir_usuario_inexistente(self, test_db):
        """Testa exclusão de usuário inexistente"""
        # Arrange
        id_inexistente = 9999
        
        # Act
        resultado = excluir_usuario(id_inexistente)
        
        # Assert
        assert resultado == False, "Exclusão de usuário inexistente deveria retornar False"

    def test_obter_todos_usuarios_paginado(self, test_db):
        """Testa obtenção paginada de usuários"""
        # Arrange
        usuarios = [
            Usuario(0, "Ana Silva", "ana@email.com", "senha1", "11111111111"),
            Usuario(0, "Bruno Costa", "bruno@email.com", "senha2", "22222222222"),
            Usuario(0, "Carlos Dias", "carlos@email.com", "senha3", "33333333333"),
            Usuario(0, "Diana Souza", "diana@email.com", "senha4", "44444444444"),
            Usuario(0, "Eduardo Lima", "eduardo@email.com", "senha5", "55555555555")
        ]
        
        for usuario in usuarios:
            inserir_usuario(usuario)
        
        # Act - primeira página
        pagina1 = obter_todos_usuarios_paginado(limite=3, offset=0)
        
        # Assert
        assert len(pagina1) == 3, "Primeira página deveria ter 3 usuários"
        assert pagina1[0].nome == "Ana Silva"
        assert pagina1[1].nome == "Bruno Costa"
        assert pagina1[2].nome == "Carlos Dias"
        
        # Act - segunda página
        pagina2 = obter_todos_usuarios_paginado(limite=3, offset=3)
        
        # Assert
        assert len(pagina2) == 2, "Segunda página deveria ter 2 usuários"
        assert pagina2[0].nome == "Diana Souza"
        assert pagina2[1].nome == "Eduardo Lima"

    def test_obter_todos_usuarios_paginado_vazio(self, test_db):
        """Testa obtenção paginada quando não há usuários"""
        # Arrange - banco vazio
        # Act
        usuarios = obter_todos_usuarios_paginado(limite=10, offset=0)
        
        # Assert
        assert len(usuarios) == 0, "Lista deveria estar vazia"

    def test_obter_usuario_por_id_existente(self, test_db):
        """Testa obtenção de usuário por ID existente"""
        # Arrange
        usuario = Usuario(0, "João Silva", "joao@email.com", "senha123", "11999998888")
        id_usuario = inserir_usuario(usuario)
        
        # Act
        usuario_db = obter_usuario_por_id(id_usuario)
        
        # Assert
        assert usuario_db is not None, "Usuário deveria existir"
        assert usuario_db.id_usuario == id_usuario
        assert usuario_db.nome == usuario.nome
        assert usuario_db.email == usuario.email
        assert usuario_db.senha == usuario.senha
        assert usuario_db.telefone == usuario.telefone

    def test_obter_usuario_por_id_inexistente(self, test_db):
        """Testa obtenção de usuário por ID inexistente"""
        # Arrange
        id_inexistente = 9999
        
        # Act
        usuario = obter_usuario_por_id(id_inexistente)
        
        # Assert
        assert usuario is None, "Usuário não deveria existir"