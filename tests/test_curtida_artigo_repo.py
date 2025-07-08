import os
import sys
from model.categoria_artigo_model import CategoriaArtigo
from model.curtida_artigo_model import CurtidaArtigo
from model.usuario_model import Usuario
from model.postagem_artigo_model import PostagemArtigo
from repo import categoria_artigo_repo, usuario_repo, postagem_artigo_repo, curtida_artigo_repo, veterinario_repo 
from datetime import date, datetime

from model.veterinario_model import Veterinario

class TestCurtidaArtigoRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = curtida_artigo_repo.criar_tabela_curtida_artigo()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_curtida(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        veterinario_repo.criar_tabela_veterinario()
        categoria_artigo_repo.criar_tabela_categoria_artigo()
        postagem_artigo_repo.criar_tabela()
        curtida_artigo_repo.criar_tabela_curtida_artigo()

        # Criar usuário para curtir
        usuario = Usuario(
            id_usuario=0, 
            nome="João", 
            email="joao@example.com", 
            senha="senha123", 
            telefone="123456789"
        )
        id_usuario = usuario_repo.inserir_usuario(usuario)
        
        # Criar veterinário para postar
        veterinario = Veterinario(
            id_usuario=0,
            nome="Dr. Silva",
            email="dr.silva@vet.com",
            senha="vet123",
            telefone="987654321",
            crmv="12345-SP",
            verificado=True,
            bio="Veterinário especialista"
        )
        id_veterinario = veterinario_repo.inserir_veterinario(veterinario)
        
        # Criar categoria
        categoria = CategoriaArtigo(
            id_categoria_artigo=0,
            nome="Cuidados",
            descricao="Artigos sobre cuidados com pets"
        )
        id_categoria = categoria_artigo_repo.inserir_categoria(categoria)
        
        # Criar postagem
        postagem = PostagemArtigo(
            id_postagem_artigo=0,
            id_veterinario=id_veterinario,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_categoria,
            data_publicacao=datetime.today().date(),
            visualizacoes=0
        )
        id_postagem = postagem_artigo_repo.inserir(postagem)
        
        # Criar curtida
        curtida = CurtidaArtigo(
            id_usuario=id_usuario, 
            id_postagem_artigo=id_postagem, 
            data_curtida=datetime.today().date()
        )
        resultado_inserir = curtida_artigo_repo.inserir_curtida_artigo(curtida)
        
        # Act
        curtida_db = curtida_artigo_repo.obter_por_id(id_usuario, id_postagem)
        
        # Assert
        assert resultado_inserir == True, "A inserção da curtida deveria retornar True"
        assert curtida_db is not None, "A curtida deveria ser encontrada"
        assert curtida_db.id_usuario == id_usuario, "O usuário da curtida não corresponde"
        assert curtida_db.id_postagem_artigo == id_postagem, "O artigo da curtida não corresponde"
        assert curtida_db.data_curtida == datetime.today().date(), "A data da curtida não corresponde"