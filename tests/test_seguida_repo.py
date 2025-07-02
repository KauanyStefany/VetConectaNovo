import os
import sys
from data.seguida_repo import *
from data.seguida_model import Seguida
from data.tutor_model import Tutor
from data.veterinario_model import Veterinario
from data.usuario_model import Usuario
from data.tutor_repo import criar_tabela_tutor, inserir_tutor
from data.veterinario_repo import criar_tabela_veterinario, inserir_veterinario
from data.usuario_repo import criar_tabela_usuario
from datetime import date

class TestSeguidaRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_seguida(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela()
        
        # Inserir usuário + veterinário
        usuario_vet = Usuario(id_usuario=0, nome="Dr. João", email="vet@email.com", senha="123", telefone="999999999")
        vet = Veterinario(**usuario_vet.__dict__, crmv="CRMV123", verificado=True, bio="Especialista")
        id_vet = inserir_veterinario(vet)
        
        # Inserir usuário + tutor
        usuario_tutor = Usuario(id_usuario=0, nome="Maria", email="maria@email.com", senha="321", telefone="888888888")
        tutor = Tutor(**usuario_tutor.__dict__)
        id_tutor = inserir_tutor(tutor)
        
        # Criar seguida
        seguida_teste = Seguida(
            id_veterinario=Veterinario(id_usuario=id_vet, nome=vet.nome, email=vet.email, senha=vet.senha, telefone=vet.telefone, crmv=vet.crmv, verificado=vet.verificado, bio=vet.bio),
            id_tutor=Tutor(id_usuario=id_tutor, nome=tutor.nome, email=tutor.email, senha=tutor.senha, telefone=tutor.telefone),
            data_inicio=date.today()
        )
        
        # Act
        resultado = inserir(seguida_teste)
        
        # Assert
        assert resultado is True, "A inserção da seguida deveria retornar True"
        seguida_db = obter_por_id(id_vet, id_tutor)
        assert seguida_db is not None, "A seguida inserida não deveria ser None"
        assert seguida_db.id_veterinario.id_usuario == id_vet, "O ID do veterinário inserido não confere"
        assert seguida_db.id_tutor.id_usuario == id_tutor, "O ID do tutor inserido não confere"

    def test_excluir_seguida(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela()
        
        # Inserir usuário + veterinário
        usuario_vet = Usuario(id_usuario=0, nome="Dr. João", email="vet@email.com", senha="123", telefone="999999999")
        vet = Veterinario(**usuario_vet.__dict__, crmv="CRMV123", verificado=True, bio="Especialista")
        id_vet = inserir_veterinario(vet)
        
        # Inserir usuário + tutor
        usuario_tutor = Usuario(id_usuario=0, nome="Maria", email="maria@email.com", senha="321", telefone="888888888")
        tutor = Tutor(**usuario_tutor.__dict__)
        id_tutor = inserir_tutor(tutor)
        
        # Criar e inserir seguida
        seguida_teste = Seguida(
            id_veterinario=Veterinario(id_usuario=id_vet, nome=vet.nome, email=vet.email, senha=vet.senha, telefone=vet.telefone, crmv=vet.crmv, verificado=vet.verificado, bio=vet.bio),
            id_tutor=Tutor(id_usuario=id_tutor, nome=tutor.nome, email=tutor.email, senha=tutor.senha, telefone=tutor.telefone),
            data_inicio=date.today()
        )
        inserir(seguida_teste)
        
        # Act
        resultado = excluir(id_vet, id_tutor)
        
        # Assert
        assert resultado is True, "A exclusão da seguida deveria retornar True"
        seguida_excluida = obter_por_id(id_vet, id_tutor)
        assert seguida_excluida is None, "A seguida excluída deveria ser None"

    def test_obter_todas_seguidas_paginado(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela()
        
        # Inserir primeiro veterinário e tutor
        usuario_vet1 = Usuario(id_usuario=0, nome="Dr. João", email="vet1@email.com", senha="123", telefone="999999999")
        vet1 = Veterinario(**usuario_vet1.__dict__, crmv="CRMV123", verificado=True, bio="Especialista")
        id_vet1 = inserir_veterinario(vet1)
        
        usuario_tutor1 = Usuario(id_usuario=0, nome="Maria", email="maria@email.com", senha="321", telefone="888888888")
        tutor1 = Tutor(**usuario_tutor1.__dict__)
        id_tutor1 = inserir_tutor(tutor1)
        
        # Inserir segundo veterinário e tutor
        usuario_vet2 = Usuario(id_usuario=0, nome="Dr. Pedro", email="vet2@email.com", senha="456", telefone="777777777")
        vet2 = Veterinario(**usuario_vet2.__dict__, crmv="CRMV456", verificado=True, bio="Cirurgião")
        id_vet2 = inserir_veterinario(vet2)
        
        usuario_tutor2 = Usuario(id_usuario=0, nome="Ana", email="ana@email.com", senha="654", telefone="666666666")
        tutor2 = Tutor(**usuario_tutor2.__dict__)
        id_tutor2 = inserir_tutor(tutor2)
        
        # Criar seguidas
        seguida1 = Seguida(
            id_veterinario=Veterinario(id_usuario=id_vet1, nome=vet1.nome, email=vet1.email, senha=vet1.senha, telefone=vet1.telefone, crmv=vet1.crmv, verificado=vet1.verificado, bio=vet1.bio),
            id_tutor=Tutor(id_usuario=id_tutor1, nome=tutor1.nome, email=tutor1.email, senha=tutor1.senha, telefone=tutor1.telefone),
            data_inicio=date.today()
        )
        seguida2 = Seguida(
            id_veterinario=Veterinario(id_usuario=id_vet2, nome=vet2.nome, email=vet2.email, senha=vet2.senha, telefone=vet2.telefone, crmv=vet2.crmv, verificado=vet2.verificado, bio=vet2.bio),
            id_tutor=Tutor(id_usuario=id_tutor2, nome=tutor2.nome, email=tutor2.email, senha=tutor2.senha, telefone=tutor2.telefone),
            data_inicio=date.today()
        )
        
        inserir(seguida1)
        inserir(seguida2)
        
        # Act
        seguidas = obter_todos_paginado(10, 0)
        
        # Assert
        assert len(seguidas) == 2, "Deveria retornar duas seguidas"
        ids_veterinarios = [s.id_veterinario.id_usuario for s in seguidas]
        assert id_vet1 in ids_veterinarios, "O ID do primeiro veterinário deveria estar presente"
        assert id_vet2 in ids_veterinarios, "O ID do segundo veterinário deveria estar presente"

    def test_obter_seguida_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_tutor()
        criar_tabela_veterinario()
        criar_tabela()
        
        # Inserir usuário + veterinário
        usuario_vet = Usuario(id_usuario=0, nome="Dr. João", email="vet@email.com", senha="123", telefone="999999999")
        vet = Veterinario(**usuario_vet.__dict__, crmv="CRMV123", verificado=True, bio="Especialista")
        id_vet = inserir_veterinario(vet)
        
        # Inserir usuário + tutor
        usuario_tutor = Usuario(id_usuario=0, nome="Maria", email="maria@email.com", senha="321", telefone="888888888")
        tutor = Tutor(**usuario_tutor.__dict__)
        id_tutor = inserir_tutor(tutor)
        
        # Criar e inserir seguida
        seguida_teste = Seguida(
            id_veterinario=Veterinario(id_usuario=id_vet, nome=vet.nome, email=vet.email, senha=vet.senha, telefone=vet.telefone, crmv=vet.crmv, verificado=vet.verificado, bio=vet.bio),
            id_tutor=Tutor(id_usuario=id_tutor, nome=tutor.nome, email=tutor.email, senha=tutor.senha, telefone=tutor.telefone),
            data_inicio=date.today()
        )
        inserir(seguida_teste)
        
        # Act
        seguida_db = obter_por_id(id_vet, id_tutor)
        
        # Assert
        assert seguida_db is not None, "A seguida obtida não deveria ser None"
        assert seguida_db.id_veterinario.id_usuario == id_vet, "O ID do veterinário obtido não confere"
        assert seguida_db.id_tutor.id_usuario == id_tutor, "O ID do tutor obtido não confere"
        assert seguida_db.data_inicio is not None, "A data de início não deveria ser None"

    def test_obter_seguida_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        # Act
        seguida_db = obter_por_id(999, 888)
        # Assert
        assert seguida_db is None, "A seguida inexistente deveria retornar None"