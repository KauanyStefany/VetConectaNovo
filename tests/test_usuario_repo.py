import pytest
from repo.usuario_repo import (
    criar_tabela as criar_tabela_usuario,
    inserir as inserir_usuario,
    atualizar as atualizar_usuario,
    atualizar_senha as atualizar_senha_usuario,
    excluir as excluir_usuario,
    obter_pagina as obter_todos_usuarios_paginado,
    obter_por_id as obter_usuario_por_id,
    obter_por_email,
    atualizar_token,
    obter_por_token,
    limpar_token,
    obter_todos_por_perfil,
    atualizar_foto
)
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
            telefone="11999998888",
            perfil="tutor",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None
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
        usuario1 = Usuario(0, "João", "email@test.com", "senha123", "11999998888", "tutor", None, None, None, None)
        usuario2 = Usuario(0, "Maria", "email@test.com", "senha456", "11888887777", "tutor", None, None, None, None)
        
        # Act
        inserir_usuario(usuario1)
        
        # Assert - deve falhar por email único
        with pytest.raises(Exception):
            inserir_usuario(usuario2)

    def test_atualizar_usuario_sucesso(self, test_db):
        """Testa atualização de usuário com sucesso"""
        # Arrange
        usuario_original = Usuario(0, "Nome Original", "original@email.com", "senha123", "11999998888", "tutor", None, None, None, None)
        id_usuario = inserir_usuario(usuario_original)
        
        # Act
        usuario_atualizado = Usuario(
            id_usuario=id_usuario,
            nome="Nome Atualizado",
            email="atualizado@email.com",
            senha="senha123",  # senha não é atualizada por atualizar_usuario
            telefone="11777776666",
            perfil="tutor",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None
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
        usuario_inexistente = Usuario(9999, "Não Existe", "nao@existe.com", "senha", "11999998888", "tutor", None, None, None, None)
        
        # Act
        resultado = atualizar_usuario(usuario_inexistente)
        
        # Assert
        assert resultado == False, "Atualização de usuário inexistente deveria retornar False"

    def test_atualizar_senha_usuario_sucesso(self, test_db):
        """Testa atualização de senha com sucesso"""
        # Arrange
        usuario = Usuario(0, "João", "joao@email.com", "senha_antiga", "11999998888", "tutor", None, None, None, None)
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
        usuario = Usuario(0, "João", "joao@email.com", "senha123", "11999998888", "tutor", None, None, None, None)
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
            Usuario(0, "Ana Silva", "ana@email.com", "senha1", "11111111111", "tutor", None, None, None, None),
            Usuario(0, "Bruno Costa", "bruno@email.com", "senha2", "22222222222", "tutor", None, None, None, None),
            Usuario(0, "Carlos Dias", "carlos@email.com", "senha3", "33333333333", "tutor", None, None, None, None),
            Usuario(0, "Diana Souza", "diana@email.com", "senha4", "44444444444", "tutor", None, None, None, None),
            Usuario(0, "Eduardo Lima", "eduardo@email.com", "senha5", "55555555555", "tutor", None, None, None, None)
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
        usuario = Usuario(0, "João Silva", "joao@email.com", "senha123", "11999998888", "tutor", None, None, None, None)
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

    def test_obter_por_email_existente(self, test_db):
        """Testa obtenção de usuário por email existente"""
        # Arrange
        usuario = Usuario(0, "João Silva", "joao.unico@email.com", "senha123", "11999998888", "tutor", None, None, None, None)
        inserir_usuario(usuario)

        # Act
        usuario_db = obter_por_email("joao.unico@email.com")

        # Assert
        assert usuario_db is not None, "Usuário deveria existir"
        assert usuario_db.email == "joao.unico@email.com"
        assert usuario_db.nome == "João Silva"

    def test_obter_por_email_inexistente(self, test_db):
        """Testa obtenção de usuário por email inexistente"""
        # Arrange & Act
        usuario = obter_por_email("naoexiste@email.com")

        # Assert
        assert usuario is None, "Usuário não deveria existir"

    def test_atualizar_token(self, test_db):
        """Testa atualização de token de redefinição"""
        # Arrange
        usuario = Usuario(0, "João", "joao.token@email.com", "senha123", "11999998888", "tutor", None, None, None, None)
        inserir_usuario(usuario)
        token = "abc123xyz"
        data_expiracao = "2025-12-31 23:59:59"

        # Act
        resultado = atualizar_token("joao.token@email.com", token, data_expiracao)

        # Assert
        assert resultado == True, "Atualização de token deveria retornar True"
        usuario_db = obter_por_email("joao.token@email.com")
        assert usuario_db.token_redefinicao == token
        assert usuario_db.data_token == data_expiracao

    def test_atualizar_token_email_inexistente(self, test_db):
        """Testa atualização de token com email inexistente"""
        # Arrange & Act
        resultado = atualizar_token("naoexiste@email.com", "token123", "2025-12-31")

        # Assert
        assert resultado == False, "Atualização de token com email inexistente deveria retornar False"

    def test_obter_por_token(self, test_db):
        """Testa obtenção de usuário por token"""
        # Arrange
        usuario = Usuario(0, "Maria", "maria.token@email.com", "senha123", "11888887777", "tutor", None, None, None, None)
        inserir_usuario(usuario)
        token = "token_unico_123"
        atualizar_token("maria.token@email.com", token, "2025-12-31")

        # Act
        usuario_db = obter_por_token(token)

        # Assert
        assert usuario_db is not None, "Usuário deveria ser encontrado pelo token"
        assert usuario_db.email == "maria.token@email.com"
        assert usuario_db.token_redefinicao == token

    def test_obter_por_token_inexistente(self, test_db):
        """Testa obtenção com token inexistente"""
        # Arrange & Act
        usuario = obter_por_token("token_que_nao_existe")

        # Assert
        assert usuario is None, "Não deveria encontrar usuário"

    def test_limpar_token(self, test_db):
        """Testa limpeza de token de redefinição"""
        # Arrange
        usuario = Usuario(0, "Carlos", "carlos.limpar@email.com", "senha123", "11777776666", "tutor", None, None, None, None)
        id_usuario = inserir_usuario(usuario)
        atualizar_token("carlos.limpar@email.com", "token123", "2025-12-31")

        # Act
        resultado = limpar_token(id_usuario)

        # Assert
        assert resultado == True, "Limpeza de token deveria retornar True"
        usuario_db = obter_usuario_por_id(id_usuario)
        assert usuario_db.token_redefinicao is None
        assert usuario_db.data_token is None

    def test_limpar_token_usuario_inexistente(self, test_db):
        """Testa limpeza de token com usuário inexistente"""
        # Arrange & Act
        resultado = limpar_token(9999)

        # Assert
        assert resultado == False, "Limpeza de token com ID inexistente deveria retornar False"

    def test_obter_todos_por_perfil(self, test_db):
        """Testa obtenção de usuários por perfil"""
        # Arrange
        usuarios = [
            Usuario(0, "Tutor 1", "tutor1@email.com", "senha1", "11111111111", "tutor", None, None, None, None),
            Usuario(0, "Tutor 2", "tutor2@email.com", "senha2", "22222222222", "tutor", None, None, None, None),
            Usuario(0, "Admin 1", "admin1@email.com", "senha3", "33333333333", "admin", None, None, None, None),
            Usuario(0, "Vet 1", "vet1@email.com", "senha4", "44444444444", "veterinario", None, None, None, None),
        ]

        for usuario in usuarios:
            inserir_usuario(usuario)

        # Act
        tutores = obter_todos_por_perfil("tutor")
        admins = obter_todos_por_perfil("admin")

        # Assert
        assert len(tutores) == 2, "Deveria haver 2 tutores"
        assert len(admins) == 1, "Deveria haver 1 admin"
        assert all(u.perfil == "tutor" for u in tutores), "Todos deveriam ser tutores"
        assert admins[0].perfil == "admin", "Deveria ser admin"

    def test_obter_todos_por_perfil_vazio(self, test_db):
        """Testa obtenção por perfil quando não há usuários"""
        # Arrange & Act
        usuarios = obter_todos_por_perfil("perfil_inexistente")

        # Assert
        assert len(usuarios) == 0, "Não deveria haver usuários"

    def test_atualizar_foto(self, test_db):
        """Testa atualização de foto do usuário"""
        # Arrange
        usuario = Usuario(0, "Pedro", "pedro.foto@email.com", "senha123", "11666665555", "tutor", None, None, None, None)
        id_usuario = inserir_usuario(usuario)
        caminho_foto = "/uploads/fotos/pedro.jpg"

        # Act
        resultado = atualizar_foto(id_usuario, caminho_foto)

        # Assert
        assert resultado == True, "Atualização de foto deveria retornar True"
        usuario_db = obter_usuario_por_id(id_usuario)
        assert usuario_db.foto == caminho_foto

    def test_atualizar_foto_usuario_inexistente(self, test_db):
        """Testa atualização de foto com usuário inexistente"""
        # Arrange & Act
        resultado = atualizar_foto(9999, "/uploads/foto.jpg")

        # Assert
        assert resultado == False, "Atualização de foto com ID inexistente deveria retornar False"