import os
import sys
from data.categoria_artigo_model import CategoriaArtigo
from data.curtida_artigo_model import CurtidaArtigo
from data.usuario_model import Usuario
from data.postagem_artigo_model import PostagemArtigo
from data import categoria_artigo_repo, usuario_repo, postagem_artigo_repo, curtida_artigo_repo, veterinario_repo 
from datetime import date, datetime

from data.veterinario_model import Veterinario

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
        postagem_artigo_repo.criar_tabela()
        curtida_artigo_repo.criar_tabela_curtida_artigo()

        usuario = Usuario(
            id_usuario=0, 
            nome="João", 
            email="joao@example.com", 
            senha="senha123", 
            telefone="123456789"
        )
        id_usuario = usuario_repo.inserir_usuario(usuario)
        postagem = PostagemArtigo(
            id=0,
            id_veterinario=1,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=2,
            data_publicacao=datetime.today().date(),
                )
        id_postagem = postagem_artigo_repo.inserir(postagem)
        curtida = CurtidaArtigo(
            id_curtida=0, 
            usuario=id_usuario, 
            artigo=id_postagem, 
            data=datetime.today().date())
        id_curtida = curtida_artigo_repo.inserir_curtida_artigo(curtida)
        # Act
        curtida_db = curtida_artigo_repo.obter_por_id(id_curtida)
        # Assert
        assert curtida_db is not None, "A curtida deveria ser encontrada"
        assert curtida_db.usuario == id_usuario, "O usuário da curtida não corresponde"
        assert curtida_db.artigo == id_postagem, "O artigo da curtida não corresponde"
        assert curtida_db.data == datetime.today().date(), "A data da curtida não corresponde"