import os
import sys
from data.categoria_artigo_model import CategoriaArtigo
from data.comentario_model import Comentario
from data.comentario_repo import *
from data.usuario_repo import criar_tabela_usuario, inserir_usuario
from data.usuario_model import Usuario
from data.veterinario_model import Veterinario


class TestComentarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela de comentários deveria retornar True"

    
    def test_inserir_comentario(self, test_db):
        # 1. Criar tabelas necessárias
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_artigo()
        criar_tabela_comentario()

        # 2. Inserir usuário
        usuario = Usuario(
            id_usuario=0,
            nome="Usuario Teste",
            email="usuario@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        id_usuario = inserir_usuario(usuario)

        # 3. Inserir veterinário
        veterinario = Veterinario(
            id_veterinario=1,
            nome="Vet Teste",
            email="vet@teste.com",
            senha="12345678",
            telefone="11999999999",
            crmv="12345",
            verificado=True,
            bio="Bio do veterinario"
        )
        inserir_veterinario(veterinario)

        # 4. Inserir categoria
        categoria = CategoriaArtigo(
            id=0,
            nome="Categoria Teste",
            descricao="Descrição da categoria"
        )
        id_categoria = inserir_categoria(categoria)

        # 5. Inserir artigo
        artigo = PostagemArtigo(
            id=0,
            veterinario=veterinario,
            titulo="Artigo Teste",
            conteudo="Conteúdo do artigo",
            categoria_artigo=categoria,
            data_publicacao="2024-01-01",
            visualizacoes=0
        )
        id_artigo = inserir_artigo(artigo)

        # 6. Criar o comentário
        comentario = Comentario(
            id=0,
            id_usuario=id_usuario,
            id_artigo=id_artigo,
            texto="Este é um comentário de teste",
            data_comentario=None,
            data_moderacao=None
        )

        # 7. Inserir comentário
        id_comentario = inserir_comentario(comentario)

        # 8. Assert: Verificar se inseriu corretamente
        assert id_comentario is not None, "A inserção do comentário deveria retornar um ID válido"

        comentarios = obter_todos_paginado(10, 0)
        assert len(comentarios) > 0, "Deveria haver pelo menos 1 comentário"

        comentario_db = comentarios[0]
        assert comentario_db.texto == comentario.texto, "O texto do comentário não confere"
        assert comentario_db.usuario.nome == usuario.nome, "O nome do usuário não confere"
        assert comentario_db.artigo.titulo == artigo.titulo, "O título do artigo não confere"
        assert comentario_db.data_comentario is not None, "A data do comentário não deveria ser None"


    def test_atualizar(self, test_db):
        # Arrange
        criar_tabela()
        comentario_teste = Comentario(
            id=1,
            id_usuario=1,  
            id_artigo=1,   
            texto="Comentário original"
        )
        inserir(comentario_teste)
        comentario_teste.texto = "Comentário atualizado"
        # Act
        resultado = atualizar(comentario_teste)
        # Assert
        assert resultado == True, "A atualização do comentário deveria retornar True"
        comentario_db = obter_todos_paginado(10, 0)[0]
        assert comentario_db.texto == "Comentário atualizado", "O texto do comentário atualizado não confere"


