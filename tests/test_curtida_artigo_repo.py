import os
import sys
from model.categoria_artigo_model import CategoriaArtigo
from model.curtida_artigo_model import CurtidaArtigo
from model.usuario_model import Usuario
from model.postagem_artigo_model import PostagemArtigo
from repo import (
    categoria_artigo_repo,
    usuario_repo,
    postagem_artigo_repo,
    curtida_artigo_repo,
    veterinario_repo,
)
from datetime import date, datetime

from model.veterinario_model import Veterinario


class TestCurtidaArtigoRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = curtida_artigo_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_curtida(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        veterinario_repo.criar_tabela()
        categoria_artigo_repo.criar_tabela()
        postagem_artigo_repo.criar_tabela()
        curtida_artigo_repo.criar_tabela()

        # Criar usuário para curtir
        usuario = Usuario(
            id_usuario=0,
            nome="João",
            email="joao@example.com",
            senha="senha123",
            telefone="123456789",
            perfil="tutor",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
        )
        id_usuario = usuario_repo.inserir(usuario)

        # Criar veterinário para postar
        veterinario = Veterinario(
            id_usuario=0,
            nome="Dr. Silva",
            email="dr.silva@vet.com",
            senha="vet123",
            telefone="987654321",
            perfil="veterinario",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="12345-SP",
            verificado=True,
            bio="Veterinário especialista",
        )
        id_veterinario = veterinario_repo.inserir(veterinario)

        # Criar categoria
        categoria = CategoriaArtigo(
            id_categoria_artigo=0, nome="Cuidados", cor="#3498DB", imagem="cuidados.png"
        )
        id_categoria = categoria_artigo_repo.inserir(categoria)

        # Criar postagem
        postagem = PostagemArtigo(
            id_postagem_artigo=0,
            id_veterinario=id_veterinario,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_categoria,
            data_publicacao=datetime.today().date(),
            visualizacoes=0,
        )
        id_postagem = postagem_artigo_repo.inserir(postagem)

        # Criar curtida
        data_hoje = datetime.now()
        curtida = CurtidaArtigo(
            id_usuario=id_usuario,
            id_postagem_artigo=id_postagem,
            data_curtida=data_hoje,
        )
        resultado_inserir = curtida_artigo_repo.inserir(curtida)

        # Act
        curtida_db = curtida_artigo_repo.obter_por_id(id_usuario, id_postagem)

        # Assert
        assert resultado_inserir == True, "A inserção da curtida deveria retornar True"
        assert curtida_db is not None, "A curtida deveria ser encontrada"
        assert (
            curtida_db.id_usuario == id_usuario
        ), "O usuário da curtida não corresponde"
        assert (
            curtida_db.id_postagem_artigo == id_postagem
        ), "O artigo da curtida não corresponde"
        assert (
            curtida_db.data_curtida.date() == data_hoje.date()
        ), "A data da curtida não corresponde"

    def test_excluir_curtida_sucesso(self, test_db):
        """Testa exclusão de curtida com sucesso"""
        # Arrange
        usuario_repo.criar_tabela()
        veterinario_repo.criar_tabela()
        categoria_artigo_repo.criar_tabela()
        postagem_artigo_repo.criar_tabela()
        curtida_artigo_repo.criar_tabela()

        # Criar usuário
        usuario = Usuario(
            0,
            "Maria",
            "maria@example.com",
            "senha123",
            "123456789",
            "tutor",
            None,
            None,
            None,
            None,
        )
        id_usuario = usuario_repo.inserir(usuario)

        # Criar veterinário
        veterinario = Veterinario(
            0,
            "Dr. Lima",
            "dr.lima@vet.com",
            "vet123",
            "987654321",
            "veterinario",
            None,
            None,
            None,
            None,
            "54321-RJ",
            True,
            "Veterinário",
        )
        id_veterinario = veterinario_repo.inserir(veterinario)

        # Criar categoria
        categoria = CategoriaArtigo(0, "Saúde", "#2ECC71", "saude.png")
        id_categoria = categoria_artigo_repo.inserir(categoria)

        # Criar postagem
        postagem = PostagemArtigo(
            0,
            id_veterinario,
            "Doenças em Cães",
            "Conteúdo",
            id_categoria,
            datetime.today().date(),
            0,
        )
        id_postagem = postagem_artigo_repo.inserir(postagem)

        # Criar curtida
        curtida = CurtidaArtigo(id_usuario, id_postagem, datetime.now())
        curtida_artigo_repo.inserir(curtida)

        # Act
        resultado = curtida_artigo_repo.excluir(id_usuario, id_postagem)

        # Assert
        assert resultado == True, "Exclusão deveria retornar True"
        curtida_db = curtida_artigo_repo.obter_por_id(id_usuario, id_postagem)
        assert curtida_db is None, "Curtida não deveria mais existir"

    def test_excluir_curtida_inexistente(self, test_db):
        """Testa exclusão de curtida inexistente"""
        # Arrange
        curtida_artigo_repo.criar_tabela()

        # Act
        resultado = curtida_artigo_repo.excluir(9999, 9999)

        # Assert
        assert (
            resultado == False
        ), "Exclusão de curtida inexistente deveria retornar False"

    def test_OBTER_PAGINA(self, test_db):
        """Testa obtenção paginada de curtidas"""
        # Arrange
        usuario_repo.criar_tabela()
        veterinario_repo.criar_tabela()
        categoria_artigo_repo.criar_tabela()
        postagem_artigo_repo.criar_tabela()
        curtida_artigo_repo.criar_tabela()

        # Criar veterinário
        veterinario = Veterinario(
            0,
            "Dr. Costa",
            "dr.costa@vet.com",
            "vet123",
            "987654321",
            "veterinario",
            None,
            None,
            None,
            None,
            "11111-SP",
            True,
            "Veterinário",
        )
        id_veterinario = veterinario_repo.inserir(veterinario)

        # Criar categoria
        categoria = CategoriaArtigo(0, "Nutrição", "#E74C3C", "nutricao.png")
        id_categoria = categoria_artigo_repo.inserir(categoria)

        # Criar postagem
        postagem = PostagemArtigo(
            0,
            id_veterinario,
            "Alimentação de Pets",
            "Conteúdo",
            id_categoria,
            datetime.today().date(),
            0,
        )
        id_postagem = postagem_artigo_repo.inserir(postagem)

        # Criar 3 usuários e 3 curtidas
        usuarios_ids = []
        for i in range(3):
            usuario = Usuario(
                0,
                f"Usuario{i}",
                f"user{i}@example.com",
                "senha",
                "111111111",
                "tutor",
                None,
                None,
                None,
                None,
            )
            id_usuario = usuario_repo.inserir(usuario)
            usuarios_ids.append(id_usuario)
            curtida = CurtidaArtigo(id_usuario, id_postagem, datetime.now())
            curtida_artigo_repo.inserir(curtida)

        # Act
        curtidas = curtida_artigo_repo.obter_pagina(limite=2, offset=0)

        # Assert
        assert len(curtidas) == 2, "Deveria retornar 2 curtidas (limite da paginação)"
        assert all(
            isinstance(c, CurtidaArtigo) for c in curtidas
        ), "Todos os itens deveriam ser CurtidaArtigo"

    def test_OBTER_PAGINA_vazio(self, test_db):
        """Testa obtenção paginada quando não há curtidas"""
        # Arrange
        curtida_artigo_repo.criar_tabela()

        # Act
        curtidas = curtida_artigo_repo.obter_pagina(limite=10, offset=0)

        # Assert
        assert len(curtidas) == 0, "Deveria retornar lista vazia"

    def test_obter_por_id_inexistente(self, test_db):
        """Testa obtenção de curtida inexistente"""
        # Arrange
        curtida_artigo_repo.criar_tabela()

        # Act
        curtida = curtida_artigo_repo.obter_por_id(9999, 9999)

        # Assert
        assert curtida is None, "Curtida inexistente deveria retornar None"
