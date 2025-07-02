from data.administrador_model import *
from data.chamado_model import Chamado
from data import chamado_repo
from data.usuario_model import Usuario
from data import usuario_repo
from data import administrador_repo
from data.usuario_sql import *
from data.administrador_model import Administrador

class TestChamadoRepo:
    def test_criar_tabelas(self, test_db):
        #Arrange
        # Act
        resultado = chamado_repo.criar_tabela_chamado()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_chamado(self, test_db):
        # Arrange
        # Cria tabelas necessárias no banco temporário
        usuario_repo.criar_tabela_usuario()
        administrador_repo.criar_tabela_administrador()
        chamado_repo.criar_tabela_chamado()  # cria tabela chamado

        # Insere usuário dummy e obtém ID
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = usuario_repo.inserir_usuario(usuario_teste)

        # Insere administrador dummy e obtém ID

        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = administrador_repo.inserir_administrador(admin_teste)

        # Cria chamado usando IDs válidos
        chamado_teste = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )

        # Act
        id_chamado_inserido = chamado_repo.inserir_chamado(chamado_teste)

        # Assert
        chamado_db = chamado_repo.obter_chamado_por_id(id_chamado_inserido)
        assert chamado_db is not None, "O chamado inserido não deveria ser None"
        assert chamado_db.id_usuario == id_usuario, "O id do usuário inserido não confere"
        assert chamado_db.id_admin == id_admin, "O id do administrador inserido não confere"
        assert chamado_db.titulo == "Título Chamado", "O título do chamado inserido não confere"
        assert chamado_db.descricao == "Descrição", "A descrição do chamado inserido não confere"
        assert chamado_db.status == "aberto", "O status do chamado inserido não confere"
        assert chamado_db.data == "2025-06-30", "A data do chamado inserido não confere"


    def test_atualizar_status_chamado(self, test_db):
        # Arrange
        # Cria tabelas necessárias no banco temporário
        usuario_repo.criar_tabela_usuario()
        administrador_repo.criar_tabela_administrador()
        chamado_repo.criar_tabela_chamado()

        # Insere usuário de teste e obtém ID
        from data.usuario_model import Usuario
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = usuario_repo.inserir_usuario(usuario_teste)

        # Insere administrador de teste e obtém ID
        from data.administrador_model import Administrador
        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = administrador_repo.inserir_administrador(admin_teste)

        # Cria chamado com IDs válidos
        chamado_teste = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )
        id_chamado_inserido = chamado_repo.inserir_chamado(chamado_teste)

        # Act
        resultado = chamado_repo.atualizar_status_chamado(id_chamado_inserido, "resolvido")

        # Assert
        assert resultado == True, "A atualização do status deveria retornar True"
        chamado_db = chamado_repo.obter_chamado_por_id(id_chamado_inserido)
        assert chamado_db.status == "resolvido", "O status do chamado atualizado não confere"

    def test_excluir_chamado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        administrador_repo.criar_tabela_administrador()
        chamado_repo.criar_tabela_chamado()

        from data.usuario_model import Usuario
        from data.administrador_model import Administrador

        # Insere usuário de teste e obtém ID
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = usuario_repo.inserir_usuario(usuario_teste)

        # Insere administrador de teste e obtém ID
        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = administrador_repo.inserir_administrador(admin_teste)

        # Insere chamado com IDs válidos
        chamado_teste = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )
        id_chamado = chamado_repo.inserir_chamado(chamado_teste)

        # Act
        resultado = chamado_repo.excluir_chamado(id_chamado)

        # Assert
        assert resultado == True, "A exclusão do chamado deveria retornar True"
        chamado_db = chamado_repo.obter_chamado_por_id(id_chamado)
        assert chamado_db is None, "O chamado deveria ter sido excluído"

    def test_obter_todos_chamados(self, test_db):
        # Arrange: cria tabelas necessárias
        usuario_repo.criar_tabela_usuario()
        administrador_repo.criar_tabela_administrador()
        chamado_repo.criar_tabela_chamado()

        from data.usuario_model import Usuario
        from data.administrador_model import Administrador

        # Insere usuário e administrador de teste
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = usuario_repo.inserir_usuario(usuario_teste)

        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = administrador_repo.inserir_administrador(admin_teste)

        # Cria dois chamados válidos
        chamado1 = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Chamado 1",
            descricao="Descrição 1",
            status="aberto",
            data="2025-06-30"
        )
        chamado2 = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Chamado 2",
            descricao="Descrição 2",
            status="aberto",
            data="2025-06-30"
        )

        chamado_repo.inserir_chamado(chamado1)
        chamado_repo.inserir_chamado(chamado2)

        # Act
        chamados = chamado_repo.obter_todos_chamados_paginado(0, 5)

        # Assert
        assert len(chamados) == 2, "Deveria retornar dois chamados"
        assert chamados[0].titulo == "Chamado 1", "O título do primeiro chamado não confere"
        assert chamados[1].titulo == "Chamado 2", "O título do segundo chamado não confere"



    def test_obter_chamado_por_id(self, test_db):
        # Arrange
        # Criar todas as tabelas necessárias
        usuario_repo.criar_tabela_usuario()
        administrador_repo.criar_tabela_administrador()
        chamado_repo.criar_tabela_chamado()

        # Inserir o usuário (id_usuario=1)
        usuario = Usuario(
            id_usuario=0,
            nome="Usuario Teste",
            email="usuario@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        id_usuario = usuario_repo.inserir_usuario(usuario)

        # Inserir o administrador (id_admin=1)
        admin = Administrador(
            id_admin=0,
            nome="Admin Teste",
            email="admin@teste.com",
            senha="12345678"
        )
        id_admin = administrador_repo.inserir_administrador(admin)

        # Criar o chamado referenciando os IDs válidos
        chamado_teste = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Chamado Teste",
            descricao="Descrição Teste",
            status="aberto",
            data="2024-01-01"
        )

        id_chamado_inserido = chamado_repo.inserir_chamado(chamado_teste)

        # Act
        chamado_db = chamado_repo.obter_chamado_por_id(id_chamado_inserido)

        # Assert
        assert chamado_db is not None
        assert chamado_db.id == id_chamado_inserido
        assert chamado_db.titulo == chamado_teste.titulo
        assert chamado_db.descricao == chamado_teste.descricao
        assert chamado_db.status == chamado_teste.status
        assert chamado_db.data == chamado_teste.data
        assert chamado_db.id_usuario == id_usuario
        assert chamado_db.id_admin == id_admin






    