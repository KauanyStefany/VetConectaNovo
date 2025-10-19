# import os  # noqa: F401
# import sys  # noqa: F401
from datetime import date
from model.categoria_artigo_model import CategoriaArtigo
from model.comentario_model import ComentarioArtigo
from model.usuario_model import Usuario
from model.veterinario_model import Veterinario
from model.postagem_artigo_model import PostagemArtigo

from repo.comentario_artigo_repo import (
    atualizar,
    criar_tabela,
    excluir,
    inserir,
    obter_pagina,
    obter_por_id,
    criar_tabela as criar_tabela_comentario,
)
from repo.usuario_repo import (
    inserir as inserir_usuario,
    criar_tabela as criar_tabela_usuario,
)
from repo.veterinario_repo import criar_tabela as criar_tabela_veterinario
from repo.categoria_artigo_repo import (
    inserir as inserir_categoria,
    criar_tabela as criar_tabela_categoria_artigo,
)
from repo.postagem_artigo_repo import (
    inserir as inserir_artigo,
    criar_tabela as criar_tabela_postagem_artigo,
)
from repo.veterinario_repo import inserir as inserir_veterinario
from datetime import datetime


class TestComentarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert (
            resultado is True
        ), "A criação da tabela de comentários deveria retornar True"

    def test_inserir(self, test_db):
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_postagem_artigo()
        criar_tabela_comentario()

        usuario_teste = Usuario(
            0,
            "Usuário Teste",
            "usuario@teste.com",
            "senha123",
            "11999999999",
            "tutor",
            None,
            None,
            None,
            )
        id_usuario = inserir_usuario(usuario_teste)
        assert id_usuario is not None
        usuario_teste.id_usuario = id_usuario  # Atualiza o ID do usuário após inserção

        # Criar veterinário diretamente (inserir_veterinario já cria o usuário)
        veterinario_teste = Veterinario(
            id_usuario=0,
            nome="Veterinário Teste",
            email="veterinario_unico@teste.com",  # Email único
            senha="senha123",
            telefone="11888888888",
            perfil="veterinario",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv="CRMV12345",
            verificado=True,
            bio="bioteste",
        )
        id_usuario_vet = inserir_veterinario(veterinario_teste)
        assert id_usuario_vet is not None
        veterinario_teste.id_usuario = id_usuario_vet

        categoria_artigo_teste = CategoriaArtigo(
            0, "Categoria Teste", "#FF5733", "categoria.png"
        )
        id_categoria_artigo = inserir_categoria(categoria_artigo_teste)
        assert id_categoria_artigo is not None

        postagem_artigo_teste = PostagemArtigo(
            id_postagem_artigo=0,
            id_veterinario=id_usuario_vet,  # ID do veterinário
            titulo="Título do Artigo Teste",
            conteudo="Conteúdo do artigo teste",
            id_categoria_artigo=id_categoria_artigo,  # ID da categoria
            data_publicacao=date(2023, 10, 1),
            visualizacoes=100,  # inteiro, não string
        )
        id_postagem_artigo = inserir_artigo(postagem_artigo_teste)
        assert id_postagem_artigo is not None
        postagem_artigo_teste.id_postagem_artigo = id_postagem_artigo

        comentario_teste = ComentarioArtigo(
            id_comentario_artigo=0,
            id_usuario=id_usuario,  # ID do usuário
            id_postagem_artigo=id_postagem_artigo,  # ID da postagem
            texto="Este é um comentário de teste",
            data_comentario=datetime.now(),
            data_moderacao=None,
        )

        id_comentario_inserido = inserir(comentario_teste)
        assert id_comentario_inserido is not None

        comentario_db = obter_por_id(id_comentario_inserido)  # type: ignore[arg-type]  # noqa: E501
        assert comentario_db is not None

        # ASSERTS
        assert comentario_db is not None, "O comentário inserido não deveria ser None"
        assert (
            comentario_db.id_usuario == id_usuario
        ), "O ID do usuário do comentário inserido não confere"
        assert (
            comentario_db.id_postagem_artigo == id_postagem_artigo
        ), "O ID do artigo do comentário inserido não confere"
        assert (
            comentario_db.texto == "Este é um comentário de teste"
        ), "O texto do comentário inserido não confere"

    def test_atualizar_comentario_sucesso(self, test_db):
        """Testa atualização de comentário com sucesso"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_postagem_artigo()
        criar_tabela_comentario()

        usuario = Usuario(
            0,
            "João",
            "joao@test.com",
            "senha123",
            "11999999999",
            "tutor",
            None,
            None,
            None,
            )
        id_usuario = inserir_usuario(usuario)
        assert id_usuario is not None

        veterinario = Veterinario(
            0,
            "Dr. Silva",
            "silva@vet.com",
            "senha123",
            "11888888888",
            "veterinario",
            None,
            None,
            None,
            
            "CRMV111",
            True,
            "Bio",
        )
        id_vet = inserir_veterinario(veterinario)
        assert id_vet is not None

        categoria = CategoriaArtigo(0, "Saúde", "#FF5733", "saude.png")
        id_categoria = inserir_categoria(categoria)
        assert id_categoria is not None

        artigo = PostagemArtigo(
            0,
            id_vet,
            "Artigo Teste",
            "Conteúdo",
            id_categoria,
            date(2023, 10, 1),
            10,
        )
        id_artigo = inserir_artigo(artigo)
        assert id_artigo is not None

        comentario = ComentarioArtigo(
            0,
            id_usuario,
            id_artigo,
            "Comentário original",
            datetime.now(),
            None,
        )
        id_comentario = inserir(comentario)
        assert id_comentario is not None

        # Act
        comentario_atualizado = ComentarioArtigo(
            id_comentario,
            id_usuario,
            id_artigo,
            "Comentário atualizado",
            datetime.now(),
            datetime.now(),
        )
        resultado = atualizar(comentario_atualizado)

        # Assert
        assert resultado is True, "Atualização deveria retornar True"
        comentario_db = obter_por_id(id_comentario)  # type: ignore[arg-type]
        assert comentario_db is not None
        assert (
            comentario_db.texto == "Comentário atualizado"
        ), "Texto deveria estar atualizado"

    def test_atualizar_comentario_inexistente(self, test_db):
        """Testa atualização de comentário inexistente"""
        # Arrange
        criar_tabela_comentario()
        comentario = ComentarioArtigo(9999, 1, 1, "Texto", datetime.now(), None)

        # Act
        resultado = atualizar(comentario)

        # Assert
        assert (
            resultado is False
        ), "Atualização de comentário inexistente deveria retornar False"

    def test_excluir_comentario_sucesso(self, test_db):
        """Testa exclusão de comentário com sucesso"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_postagem_artigo()
        criar_tabela_comentario()

        usuario = Usuario(
            0,
            "Maria",
            "maria@test.com",
            "senha123",
            "11999999999",
            "tutor",
            None,
            None,
            None,
            )
        id_usuario = inserir_usuario(usuario)
        assert id_usuario is not None

        veterinario = Veterinario(
            0,
            "Dr. Costa",
            "costa@vet.com",
            "senha123",
            "11888888888",
            "veterinario",
            None,
            None,
            None,
            
            "CRMV222",
            True,
            "Bio",
        )
        id_vet = inserir_veterinario(veterinario)

        categoria = CategoriaArtigo(0, "Nutrição", "#00FF00", "nutricao.png")
        id_categoria = inserir_categoria(categoria)
        assert id_categoria is not None

        assert id_vet is not None
        artigo = PostagemArtigo(
            0,
            id_vet,
            "Nutrição Canina",
            "Conteúdo",
            id_categoria,
            date(2023, 10, 1),
            20,
        )
        id_artigo = inserir_artigo(artigo)
        assert id_artigo is not None

        comentario = ComentarioArtigo(
            0, id_usuario, id_artigo, "Ótimo artigo!", datetime.now(), None
        )
        id_comentario = inserir(comentario)

        # Act
        resultado = excluir(id_comentario)  # type: ignore[arg-type]

        # Assert
        assert resultado is True, "Exclusão deveria retornar True"
        comentario_db = obter_por_id(id_comentario)  # type: ignore[arg-type]
        assert comentario_db is None, "Comentário não deveria mais existir"

    def test_excluir_comentario_inexistente(self, test_db):
        """Testa exclusão de comentário inexistente"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_postagem_artigo()
        criar_tabela_comentario()

        # Act
        resultado = excluir(9999)

        # Assert
        assert (
            resultado is False
        ), "Exclusão de comentário inexistente deveria retornar False"

    def test_OBTER_PAGINA(self, test_db):
        """Testa obtenção paginada de comentários"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_postagem_artigo()
        criar_tabela_comentario()

        usuario = Usuario(
            0,
            "Pedro",
            "pedro@test.com",
            "senha123",
            "11999999999",
            "tutor",
            None,
            None,
            None,
            )
        id_usuario = inserir_usuario(usuario)
        assert id_usuario is not None

        veterinario = Veterinario(
            0,
            "Dr. Lima",
            "lima@vet.com",
            "senha123",
            "11888888888",
            "veterinario",
            None,
            None,
            None,
            
            "CRMV333",
            True,
            "Bio",
        )
        id_vet = inserir_veterinario(veterinario)

        categoria = CategoriaArtigo(0, "Comportamento", "#0000FF", "comportamento.png")
        id_categoria = inserir_categoria(categoria)
        assert id_categoria is not None

        assert id_vet is not None
        artigo = PostagemArtigo(
            0,
            id_vet,
            "Comportamento Felino",
            "Conteúdo",
            id_categoria,
            date(2023, 10, 1),
            30,
        )
        id_artigo = inserir_artigo(artigo)
        assert id_artigo is not None

        # Criar 5 comentários
        for i in range(5):
            comentario = ComentarioArtigo(
                0,
                id_usuario,
                id_artigo,
                f"Comentário {i}",
                datetime.now(),
                None,
            )
            inserir(comentario)

        # Act
        comentarios = obter_pagina(limite=3, offset=0)

        # Assert
        assert len(comentarios) == 3, "Deveria retornar 3 comentários"
        assert all(
            isinstance(c, ComentarioArtigo) for c in comentarios
        ), "Todos deveriam ser Comentario"

    def test_OBTER_PAGINA_vazio(self, test_db):
        """Testa obtenção paginada quando não há comentários"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_postagem_artigo()
        criar_tabela_comentario()

        # Act
        comentarios = obter_pagina(limite=10, offset=0)

        # Assert
        assert len(comentarios) == 0, "Deveria retornar lista vazia"

    def test_obter_por_id_inexistente(self, test_db):
        """Testa obtenção de comentário inexistente"""
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_postagem_artigo()
        criar_tabela_comentario()

        # Act
        comentario = obter_por_id(9999)

        # Assert
        assert comentario is None, "Comentário inexistente deveria retornar None"
