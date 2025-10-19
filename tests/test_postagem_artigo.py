from datetime import datetime
# import os  # noqa: F401
# import sys  # noqa: F401
from repo import (
    usuario_repo,
    veterinario_repo,
    categoria_artigo_repo,
    postagem_artigo_repo,
)
from model.categoria_artigo_model import CategoriaArtigo
from model.postagem_artigo_model import PostagemArtigo
from model.veterinario_model import Veterinario
# from util.db_util import get_connection  # noqa: F401


class TestPostagemArtigoRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = postagem_artigo_repo.criar_tabela()
        # Assert
        assert resultado is True, "A criação da tabela deveria retornar True"

    def test_inserir_postagem_artigo(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        veterinario_repo.criar_tabela()
        categoria_artigo_repo.criar_tabela()
        postagem_artigo_repo.criar_tabela()

        vet = Veterinario(
            id_usuario=0,
            nome="Dr. João",
            email="joao1@email.com",
            senha="123",
            telefone="999999999",
            perfil="veterinario",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV123",
            verificado=True,
            bio="Especialista em felinos",
        )
        id_vet = veterinario_repo.inserir(vet)
        assert id_vet is not None

        categoria = CategoriaArtigo(
            id_categoria_artigo=0,
            nome="Saúde Felina",
            cor="#27AE60",
            imagem="saude_felina.png",
        )
        id_cat = categoria_artigo_repo.inserir(categoria)
        assert id_cat is not None

        postagem = PostagemArtigo(
            id_postagem_artigo=0,
            id_veterinario=id_vet,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_cat,
            data_publicacao=datetime.today().date(),
            visualizacoes=0,
        )
        # Act
        id_post = postagem_artigo_repo.inserir(postagem)
        # Assert
        assert id_post is not None, "A inserção deveria retornar um ID válido"
        postagem_db = postagem_artigo_repo.obter_por_id(id_post)  # type: ignore[arg-type]  # noqa: E501
        assert (
            postagem_db is not None
        ), "A postagem deveria ser inserida e recuperada"
        assert (
            postagem_db.titulo == postagem.titulo
        ), "O título da postagem recuperada está incorreto"
        assert (
            postagem_db.conteudo == postagem.conteudo
        ), "O conteúdo da postagem recuperada está incorreto"
        assert (
            postagem_db.id_categoria_artigo == postagem.id_categoria_artigo
        ), "A categoria da postagem recuperada está incorreta"
        assert (
            postagem_db.data_publicacao is not None
        ), "A data de publicação não deveria ser None"
        assert (
            postagem_db.visualizacoes == postagem.visualizacoes
        ), "As visualizações da postagem recuperada estão incorretas"

    def test_obter_por_id(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        veterinario_repo.criar_tabela()
        categoria_artigo_repo.criar_tabela()
        postagem_artigo_repo.criar_tabela()

        vet = Veterinario(
            id_usuario=0,
            nome="Dr. João",
            email="joao2@email.com",
            senha="123",
            telefone="999999999",
            perfil="veterinario",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV123",
            verificado=True,
            bio="Especialista em felinos",
        )
        id_vet = veterinario_repo.inserir(vet)
        assert id_vet is not None

        categoria = CategoriaArtigo(
            id_categoria_artigo=0,
            nome="Saúde Felina",
            cor="#27AE60",
            imagem="saude_felina.png",
        )
        id_cat = categoria_artigo_repo.inserir(categoria)
        assert id_cat is not None

        postagem = PostagemArtigo(
            id_postagem_artigo=0,
            id_veterinario=id_vet,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_cat,
            data_publicacao=datetime.today().date(),
            visualizacoes=0,
        )
        id_post = postagem_artigo_repo.inserir(postagem)
        # Act
        postagem_db = postagem_artigo_repo.obter_por_id(id_post)  # type: ignore[arg-type]  # noqa: E501
        # Assert
        assert (
            postagem_db is not None
        ), "A postagem deveria ser inserida e recuperada"
        assert (
            postagem_db.titulo == postagem.titulo
        ), "O título da postagem recuperada está incorreto"
        assert (
            postagem_db.conteudo == postagem.conteudo
        ), "O conteúdo da postagem recuperada está incorreto"
        assert (
            postagem_db.id_categoria_artigo == postagem.id_categoria_artigo
        ), "A categoria da postagem recuperada está incorreta"
        assert (
            postagem_db.data_publicacao is not None
        ), "A data de publicação não deveria ser None"
        assert (
            postagem_db.visualizacoes == postagem.visualizacoes
        ), "As visualizações da postagem recuperada estão incorretas"

    def test_atualizar_postagem_artigo(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        veterinario_repo.criar_tabela()
        categoria_artigo_repo.criar_tabela()
        postagem_artigo_repo.criar_tabela()
        vet = Veterinario(
            id_usuario=0,
            nome="Dr. João",
            email="joao3@email.com",
            senha="123",
            telefone="999999999",
            perfil="veterinario",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV123",
            verificado=True,
            bio="Especialista em felinos",
        )
        id_vet = veterinario_repo.inserir(vet)
        assert id_vet is not None
        categoria = CategoriaArtigo(
            id_categoria_artigo=0,
            nome="Saúde Felina",
            cor="#27AE60",
            imagem="saude_felina.png",
        )
        id_cat = categoria_artigo_repo.inserir(categoria)
        assert id_cat is not None
        postagem = PostagemArtigo(
            id_postagem_artigo=0,
            id_veterinario=id_vet,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_cat,
            data_publicacao=datetime.today().date(),
            visualizacoes=0,
        )
        id_post = postagem_artigo_repo.inserir(postagem)
        postagem_db = postagem_artigo_repo.obter_por_id(id_post)  # type: ignore[arg-type]  # noqa: E501
        assert postagem_db is not None
        # Act
        postagem_db.titulo = "Vacinação de Gatos Atualizado"
        postagem_db.conteudo = "Texto do artigo atualizado"
        postagem_artigo_repo.atualizar(postagem_db)
        # Assert
        postagem_atualizada = postagem_artigo_repo.obter_por_id(id_post)  # type: ignore[arg-type]  # noqa: E501
        assert (
            postagem_atualizada is not None
        ), "A postagem deveria ser inserida e recuperada"
        assert (
            postagem_atualizada.titulo == "Vacinação de Gatos Atualizado"
        ), "O título da postagem atualizada está incorreto"
        assert (
            postagem_atualizada.conteudo == "Texto do artigo atualizado"
        ), "O conteúdo da postagem atualizada está incorreto"
        assert (
            postagem_atualizada.id_categoria_artigo == id_cat
        ), "A categoria da postagem atualizada está incorreta"
        assert (
            postagem_atualizada.data_publicacao is not None
        ), "A data de publicação não deveria ser None"
        assert (
            postagem_atualizada.visualizacoes == 0
        ), "As visualizações da postagem atualizada estão incorretas"

    def test_excluir_postagem_artigo(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        veterinario_repo.criar_tabela()
        categoria_artigo_repo.criar_tabela()
        postagem_artigo_repo.criar_tabela()
        vet = Veterinario(
            id_usuario=0,
            nome="Dr. João",
            email="joao4@email.com",
            senha="123",
            telefone="999999999",
            perfil="veterinario",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV123",
            verificado=True,
            bio="Especialista em felinos",
        )
        id_vet = veterinario_repo.inserir(vet)
        assert id_vet is not None
        categoria = CategoriaArtigo(
            id_categoria_artigo=0,
            nome="Saúde Felina",
            cor="#27AE60",
            imagem="saude_felina.png",
        )
        id_cat = categoria_artigo_repo.inserir(categoria)
        assert id_cat is not None
        postagem = PostagemArtigo(
            id_postagem_artigo=0,
            id_veterinario=id_vet,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_cat,
            data_publicacao=datetime.today().date(),
            visualizacoes=0,
        )
        id_post = postagem_artigo_repo.inserir(postagem)
        # Act
        excluiu = postagem_artigo_repo.excluir(id_post)  # type: ignore[arg-type]  # noqa: E501
        # Assert
        assert excluiu is True, "A exclusão deveria retornar True"
        postagem_excluida = postagem_artigo_repo.obter_por_id(id_post)  # type: ignore[arg-type]  # noqa: E501
        assert (
            postagem_excluida is None
        ), "A postagem deveria ser excluída e não recuperada"

    def test_OBTER_PAGINA(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        veterinario_repo.criar_tabela()
        categoria_artigo_repo.criar_tabela()
        postagem_artigo_repo.criar_tabela()
        vet = Veterinario(
            id_usuario=0,
            nome="Dr. João",
            email="joao5@email.com",
            senha="123",
            telefone="999999999",
            perfil="veterinario",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV123",
            verificado=True,
            bio="Especialista em felinos",
        )
        id_vet = veterinario_repo.inserir(vet)
        categoria = CategoriaArtigo(
            id_categoria_artigo=0,
            nome="Saúde Felina",
            cor="#27AE60",
            imagem="saude_felina.png",
        )
        id_cat = categoria_artigo_repo.inserir(categoria)
        assert id_vet is not None
        assert id_cat is not None
        ids_posts = []
        for i in range(10):
            postagem = PostagemArtigo(
                id_postagem_artigo=0,
                id_veterinario=id_vet,
                titulo=f"Vacinação de Gatos {i}",
                conteudo=f"Texto do artigo {i}",
                id_categoria_artigo=id_cat,
                data_publicacao=datetime.today().date(),
                visualizacoes=i * 10,
            )
            id_post = postagem_artigo_repo.inserir(postagem)
            ids_posts.append(id_post)  # type: ignore[arg-type]
        # Act
        pagina1 = postagem_artigo_repo.obter_pagina(1, 6)
        pagina2 = postagem_artigo_repo.obter_pagina(2, 6)
        # Assert
        assert (
            len(pagina1) == 6
        ), "A primeira página deveria conter 6 postagens"
        assert len(pagina2) == 4, "A segunda página deveria conter 4 postagens"
        assert (
            pagina1[0].id_postagem_artigo == ids_posts[0]
        ), "A primeira postagem da primeira página está incorreta"
        assert (
            pagina2[0].id_postagem_artigo == ids_posts[6]
        ), "A primeira postagem da segunda página está incorreta"
