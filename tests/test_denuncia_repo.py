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

    
      
