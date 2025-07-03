import os
import sys
from data.curtida_artigo_repo import *
from data.curtida_artigo_model import CurtidaArtigo
from data.usuario_model import Usuario
from data.usuario_repo import *
from data.postagem_artigo_model import PostagemArtigo
from data.postagem_artigo_repo import *
from datetime import date

class TestCurtidaArtigoRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_curtida_artigo()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_curtida(self, test_db):
        # Arrange
        criar_tabela_usuario() 
        criar_tabela()       
        criar_tabela_curtida_artigo()
        usuario_teste = Usuario(id_usuario=1,
                                nome="Usuario Teste",
                                email="joao@gmail.com",
                                senha="123456",
                                telefone="999999999")
        artigo_teste = PostagemArtigo(id=1,
                                      titulo="Artigo Teste",
                                      conteudo="Conteúdo do artigo de teste",
                                      categoria_artigo=None,  # Supondo que a categoria seja opcional
                                      data_publicacao=str(date.today()),
                                      visualizacoes=0,
                                      veterinario=None)
        curtida_teste = CurtidaArtigo(
                                      usuario=usuario_teste,
                                      artigo=artigo_teste,
                                      data_curtida=str(date.today()))
        
        # Act
        resultado_insercao = inserir_curtida_artigo(curtida_teste)
        
        # Assert
        assert resultado_insercao == True, "A inserção da curtida deveria retornar True"
        curtida_db = obter_por_id(1, 1)
        assert curtida_db is not None, "A curtida inserida não deveria ser None"
        assert curtida_db.id_usuario == 1, "O ID do usuário da curtida inserida deveria ser 1"
        assert curtida_db.artigo.id == 1, "O ID do artigo da curtida inserida deveria ser 1"

    def test_excluir_curtida(self, test_db):
        # Arrange
        criar_tabela()
        usuario_teste = Usuario(id=1, nome="Usuario Teste")
        artigo_teste = PostagemArtigo(id=1, titulo="Artigo Teste")
        curtida_teste = CurtidaArtigo(
            usuario=usuario_teste,
            artigo=artigo_teste,
            data_curtida=str(date.today())
        )
        inserir(curtida_teste)
        
        # Act
        resultado = excluir_curtida(1, 1)
        
        # Assert
        assert resultado == True, "A exclusão da curtida deveria retornar True"
        curtida_excluida = obter_por_id(1, 1)
        assert curtida_excluida == None, "A curtida excluída deveria ser None"

    def test_obter_todas_curtidas_paginado(self, test_db):
        # Arrange
        criar_tabela()
        usuario1 = Usuario(id=1, nome="Usuario 1")
        usuario2 = Usuario(id=2, nome="Usuario 2")
        artigo1 = PostagemArtigo(id=1, titulo="Artigo 1")
        artigo2 = PostagemArtigo(id=2, titulo="Artigo 2")
        
        curtida1 = CurtidaArtigo(
            usuario=usuario1,
            artigo=artigo1,
            data_curtida=str(date.today())
        )
        curtida2 = CurtidaArtigo(
            usuario=usuario2,
            artigo=artigo2,
            data_curtida=str(date.today())
        )
        
        inserir(curtida1)
        inserir(curtida2)
        
        # Act
        curtidas = obter_todos_paginado(5, 0)
        
        # Assert
        assert len(curtidas) == 2, "Deveria retornar duas curtidas"
        assert curtidas[0].usuario.id in [1, 2], "O ID do usuário da primeira curtida deveria ser 1 ou 2"
        assert curtidas[1].usuario.id in [1, 2], "O ID do usuário da segunda curtida deveria ser 1 ou 2"

    def test_obter_curtida_por_id(self, test_db):
        # Arrange
        criar_tabela()
        usuario_teste = Usuario(id=1, nome="Usuario Teste")
        artigo_teste = PostagemArtigo(id=1, titulo="Artigo Teste")
        curtida_teste = CurtidaArtigo(
            usuario=usuario_teste,
            artigo=artigo_teste,
            data_curtida=str(date.today())
        )
        inserir(curtida_teste)
        
        # Act
        curtida_db = obter_por_id(1, 1)
        
        # Assert
        assert curtida_db is not None, "A curtida obtida não deveria ser diferente de None"
        assert curtida_db.usuario.id == 1, "O ID do usuário da curtida obtida não confere"
        assert curtida_db.artigo.id == 1, "O ID do artigo da curtida obtida não confere"
        assert curtida_db.data_curtida is not None, "A data da curtida não deveria ser None"

    def test_obter_curtida_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        
        # Act
        curtida_inexistente = obter_por_id(999, 999)
        
        # Assert
        assert curtida_inexistente is None, "Curtida inexistente deveria retornar None"

    def test_excluir_curtida_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        
        # Act
        resultado = excluir_curtida(999, 999)
        
        # Assert
        assert resultado == False, "Excluir curtida inexistente deveria retornar False"