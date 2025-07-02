import os
import sys
from data.administrador_model import Administrador
from data.denuncia_repo import *
from data.usuario_repo import *
from data.administrador_repo import *
from data.denuncia_model import Denuncia
from data.usuario_model import Usuario

class TestDenunciaRepo:
    def test_criar_tabela_denuncia(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_denuncia()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_denuncia(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia
        
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(
            id_usuario=0, nome="Usuário Teste", email="teste@teste.com", senha="12345678", telefone="12345678900"
        ))
    
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(
            id_admin=0, nome="Admin Teste", email="admin@teste.com", senha="admin123"
        ))
        
        # Cria uma denúncia com os IDs válidos
        denuncia_teste = Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste",
            data_denuncia="2025-06-30",
            status="pendente"  
        )
        
        # Act
        id_denuncia_inserida = inserir_denuncia(denuncia_teste)
        
        # Assert
        denuncia_db = obter_denuncia_por_id(id_denuncia_inserida)
        assert denuncia_db is not None, "A denúncia inserida não deveria ser None"
        assert denuncia_db.id_usuario == usuario_id, "O ID do usuário da denúncia inserida não confere"
        assert denuncia_db.id_denuncia == 1, "A denúncia inserida deveria ter um ID igual a 1"
        assert denuncia_db.motivo == "Motivo Teste", "O motivo da denuncia da denúncia inserida não confere"
        assert denuncia_db.status == "pendente", "O status da denúncia inserida não confere"

    def test_atualizar_denuncia(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia   
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(id_usuario=0, nome="Usuário Teste", email="usuario@gmail.com", senha="12345678", telefone="12345678900"))
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(id_admin=0, nome="Admin Teste", email="admin@gmail.com", senha="admin123"))
        # Insere uma denúncia
        denuncia_id = inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste",
            data_denuncia="2025-30-06",
            status="pendente"
        ))
        # Atualiza a denúncia
        denuncia_atualizada = Denuncia(
            id_denuncia=denuncia_id,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Atualizado",
            data_denuncia="2025-01-07",
            status="aprovada"
        )
        # Act
        resultado = atualizar_denuncia(denuncia_atualizada)
        # Assert
        assert resultado == True, "A atualização da denúncia deveria retornar True"
        denuncia_db = obter_denuncia_por_id(denuncia_id)
        assert denuncia_db is not None, "A denúncia atualizada não deveria ser None"    
        assert denuncia_db.id_denuncia == denuncia_id, "O ID da denúncia atualizada não confere"
        assert denuncia_db.motivo == "Motivo Atualizado", "O motivo da denúncia atualizada não confere"
        assert denuncia_db.data_denuncia == "2025-01-07", "A data da denúncia atualizada não confere"
        assert denuncia_db.status == "aprovada", "O status da denúncia atualizada não confere"

    def test_excluir_denuncia(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(id_usuario=0, nome="Usuário Teste", email="usuario@gmail.com", senha="12345678", telefone="12345678900"))
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(id_admin=0, nome="Admin Teste", email="admin@gmail.com", senha="admin123"))
        # Insere uma denúncia
        denuncia_id = inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste",
            data_denuncia="2025-06-30",
            status="pendente"
        ))
        # Act
        resultado = excluir_denuncia(denuncia_id)
        # Assert
        assert resultado == True, "A exclusão da denúncia deveria retornar True"
        denuncia_db = obter_denuncia_por_id(denuncia_id)
        assert denuncia_db is None, "A denúncia excluída deveria ser None"

    def test_obter_todas_denuncias_paginadas(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia   
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(id_usuario=0, nome="Usuário Teste", email="usuario@gmail.com", senha="12345678", telefone="12345678900"))
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(id_admin=0, nome="Admin Teste", email="admin@gmail.com", senha="admin123"))
        # Insere uma denúncia
        inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste 1",
            data_denuncia="2025-06-30",
            status="pendente"
        ))
        inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste 2",
            data_denuncia="2025-07-01",
            status="aprovada"
        ))
        inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste 3",
            data_denuncia="2025-07-02",
            status="rejeitada"
        ))
        # Act
        denuncias = obter_todas_denuncias_paginadas(limite=2, offset=0)
        # Assert    
        assert len(denuncias) == 2, "Deveria retornar 2 denúncias"
        motivos = [d.motivo for d in denuncias]
        assert "Motivo Teste 1" in motivos, "Motivo Teste 1 não encontrado"
        assert "Motivo Teste 2" in motivos, "Motivo Teste 2 não encontrado"


    

    def test_obter_denuncia_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(id_usuario=0, nome="Usuário Teste", email="emailteste@gmail.com",senha="12345678", telefone="12345678900"))
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(id_admin=0, nome="Admin Teste", email="adminTeste@gmail.com", senha="admin123"))
        # Insere uma denúncia
        denuncia_id = inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste",
            data_denuncia="2025-06-30",
            status="pendente"
        ))
        # Act
        denuncia_obtida = obter_denuncia_por_id(denuncia_id)
        # Assert
        assert denuncia_obtida is not None, "A denúncia obtida não deveria ser None"
        assert denuncia_obtida.id_denuncia == denuncia_id, "O ID da denúncia obtida não confere"
        assert denuncia_obtida.id_usuario == usuario_id, "O ID do usuário da denúncia obtida não confere"
        assert denuncia_obtida.id_admin == admin_id, "O ID do administrador da denúncia obtida não confere"
        assert denuncia_obtida.motivo == "Motivo Teste", "O motivo da denúncia obtida não confere"
        assert denuncia_obtida.data_denuncia == "2025-06-30", "A data da denúncia obtida não confere"
        assert denuncia_obtida.status == "pendente", "O status da denúncia obtida não confere"

 


    
      
