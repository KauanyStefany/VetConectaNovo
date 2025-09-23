import pytest
import time
from app.database.repositories.usuario_repo import *
from app.database.models.usuario_model import Usuario

def unique_email(prefix="test"):
    """Gera um email único para testes"""
    timestamp = str(int(time.time() * 1000000))
    return f"{prefix}_{timestamp}@test.com"


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
            email=unique_email("joao.silva"),
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
        email_compartilhado = unique_email("shared")
        usuario1 = Usuario(id_usuario=0, nome="João", email=email_compartilhado, senha="senha123", telefone="11999998888")
        usuario2 = Usuario(id_usuario=0, nome="Maria", email=email_compartilhado, senha="senha456", telefone="11888887777")
        
        # Act
        inserir_usuario(usuario1)
        
        # Assert - deve falhar por email único
        with pytest.raises(Exception):
            inserir_usuario(usuario2)

    def test_atualizar_usuario_sucesso(self, test_db):
        """Testa atualização de usuário com sucesso"""
        # Arrange
        usuario_original = Usuario(id_usuario=0, nome="Nome Original", email=unique_email("original"), senha="senha123", telefone="11999998888")
        id_usuario = inserir_usuario(usuario_original)
        
        # Act
        usuario_atualizado = Usuario(
            id_usuario=id_usuario,
            nome="Nome Atualizado",
            email=unique_email("atualizado"),
            senha="senha123",  # senha não é atualizada por atualizar_usuario
            telefone="11777776666"
        )
        resultado = atualizar_usuario(usuario_atualizado)
        
        # Assert
        assert resultado == True, "Atualização deveria retornar True"
        
        usuario_db = obter_usuario_por_id(id_usuario)
        assert usuario_db.nome == "Nome Atualizado"
        assert usuario_db.email == usuario_atualizado.email
        assert usuario_db.telefone == "11777776666"
        assert usuario_db.senha == "senha123"  # senha não deve mudar

    def test_atualizar_usuario_inexistente(self, test_db):
        """Testa atualização de usuário inexistente"""
        # Arrange
        usuario_inexistente = Usuario(id_usuario=0, nome="Não Existe", email=unique_email("naoexiste"), senha="senha", telefone="11999998888")
        
        # Act
        resultado = atualizar_usuario(usuario_inexistente)
        
        # Assert
        assert resultado == False, "Atualização de usuário inexistente deveria retornar False"

    def test_atualizar_senha_usuario_sucesso(self, test_db):
        """Testa atualização de senha com sucesso"""
        # Arrange
        usuario = Usuario(id_usuario=0, nome="João", email=unique_email("joao.senha"), senha="senha_antiga", telefone="11999998888")
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
        usuario = Usuario(id_usuario=0, nome="João", email=unique_email("joao.excluir"), senha="senha123", telefone="11999998888")
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
            Usuario(id_usuario=0, nome="Ana Silva", email=unique_email("ana"), senha="senha1", telefone="11111111111"),
            Usuario(id_usuario=0, nome="Bruno Costa", email=unique_email("bruno"), senha="senha2", telefone="22222222222"),
            Usuario(id_usuario=0, nome="Carlos Dias", email=unique_email("carlos"), senha="senha3", telefone="33333333333"),
            Usuario(id_usuario=0, nome="Diana Souza", email=unique_email("diana"), senha="senha4", telefone="44444444444"),
            Usuario(id_usuario=0, nome="Eduardo Lima", email=unique_email("eduardo"), senha="senha5", telefone="55555555555")
        ]
        
        for usuario in usuarios:
            inserir_usuario(usuario)
        
        # Act - primeira página
        pagina1 = obter_todos_usuarios_paginado(limite=3, offset=0)

        # Assert
        assert len(pagina1) >= 3, "Primeira página deveria ter pelo menos 3 usuários"

        # Act - segunda página
        pagina2 = obter_todos_usuarios_paginado(limite=3, offset=3)

        # Assert
        assert len(pagina2) >= 2, "Segunda página deveria ter pelo menos 2 usuários"

    def test_obter_todos_usuarios_paginado_vazio(self, test_db):
        """Testa obtenção paginada quando não há usuários"""
        # Arrange - banco vazio
        # Act
        usuarios = obter_todos_usuarios_paginado(limite=10, offset=0)
        
        # Assert
        assert isinstance(usuarios, list), "Deveria retornar uma lista"

    def test_obter_usuario_por_id_existente(self, test_db):
        """Testa obtenção de usuário por ID existente"""
        # Arrange
        usuario = Usuario(id_usuario=0, nome="João Silva", email=unique_email("joao.busca"), senha="senha123", telefone="11999998888")
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