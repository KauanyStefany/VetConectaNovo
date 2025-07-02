import os
import sys
from data.categoria_artigo_repo import *
from data.categoria_artigo_model import CategoriaArtigo
from data.postagem_artigo_repo import *
from data.postagem_artigo_model import PostagemArtigo
from data.veterinario_repo import *
from data.veterinario_model import Veterinario
from util import get_connection

class TestPostagemArtigoRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_postagem_artigo(self, test_db):
        # Arrange
        # Criar tabelas necessárias
        criar_tabela_categoria_artigo()
        criar_tabela_veterinario()  # Corrigido: era criar_tabela_tutor()
        criar_tabela()

        conn = get_connection()
        cursor = conn.cursor()

        # Inserir veterinário
        cursor.execute(
            "INSERT INTO veterinario (id_usuario, nome, email, senha, telefone, crmv, verificado, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (1, "Dr. João", "joao@email.com", "123", "999999999", "CRMV123", True, "Especialista em felinos")
        )

        # Inserir categoria
        cursor.execute(
            "INSERT INTO categoria_artigo (id, nome, descricao) VALUES (?, ?, ?)",
            (1, "Saúde", "Descrição")
        )

        conn.commit()
        conn.close()

        # Criar objeto PostagemArtigo para teste
        veterinario_teste = Veterinario(
            id_usuario=1,
            nome="Dr. João",
            email="joao@email.com",
            senha="123",
            telefone="999999999",
            crmv="CRMV123",
            verificado=True,
            bio="Especialista em felinos"
        )
        
        categoria_teste = CategoriaArtigo(1, "Saúde", "Descrição")
        
        postagem_teste = PostagemArtigo(
            id=0,
            veterinario=veterinario_teste,
            titulo="Título",
            conteudo="Conteúdo",
            categoria_artigo=categoria_teste,
            data_publicacao="2025-06-30",
            visualizacoes=0
        )

        # Act
        id_postagem_criada = inserir(postagem_teste)

        # Assert
        postagem_db = obter_por_id(id_postagem_criada)
        assert postagem_db is not None, "A postagem retornada não deveria ser None"
        assert postagem_db.id == id_postagem_criada, f"O ID da postagem criada deveria ser {id_postagem_criada}"
        assert postagem_db.titulo == "Título", "O título da postagem não confere"
        assert postagem_db.conteudo == "Conteúdo", "O conteúdo da postagem não confere"
        assert postagem_db.veterinario.nome == "Dr. João", "O nome do veterinário não confere"
        assert postagem_db.categoria_artigo.nome == "Saúde", "A categoria do artigo não confere"
        # Note: data_publicacao será definida automaticamente pelo banco
        assert postagem_db.visualizacoes == 0, "O número de visualizações deveria ser 0"

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_inexistente = 999

        # Act
        resultado = obter_por_id(id_inexistente)

        # Assert
        assert resultado is None, "Deveria retornar None para ID inexistente"

    def test_atualizar_postagem_artigo(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        criar_tabela_veterinario()
        criar_tabela()

        conn = get_connection()
        cursor = conn.cursor()

        # Inserir dados necessários
        cursor.execute(
            "INSERT INTO veterinario (id_usuario, nome, email, senha, telefone, crmv, verificado, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (1, "Dr. João", "joao@email.com", "123", "999999999", "CRMV123", True, "Especialista em felinos")
        )
        cursor.execute(
            "INSERT INTO categoria_artigo (id, nome, descricao) VALUES (?, ?, ?)",
            (1, "Saúde", "Descrição")
        )
        cursor.execute(
            "INSERT INTO categoria_artigo (id, nome, descricao) VALUES (?, ?, ?)",
            (2, "Comportamento", "Nova Descrição")
        )
        conn.commit()
        conn.close()

        # Criar e inserir postagem inicial
        veterinario_teste = Veterinario(1, "Dr. João", "joao@email.com", "123", "999999999", "CRMV123", True, "Especialista em felinos")
        categoria_inicial = CategoriaArtigo(1, "Saúde", "Descrição")
        
        postagem_inicial = PostagemArtigo(0, veterinario_teste, "Título Original", "Conteúdo Original", categoria_inicial, "2025-06-30", 0)
        id_postagem = inserir(postagem_inicial)

        # Criar postagem atualizada
        categoria_nova = CategoriaArtigo(2, "Comportamento", "Nova Descrição")
        postagem_atualizada = PostagemArtigo(id_postagem, veterinario_teste, "Título Atualizado", "Conteúdo Atualizado", categoria_nova, "2025-06-30", 5)

        # Act
        resultado = atualizar(postagem_atualizada)

        # Assert
        assert resultado == True, "A atualização deveria retornar True"
        
        postagem_db = obter_por_id(id_postagem)
        assert postagem_db.titulo == "Título Atualizado", "O título não foi atualizado"
        assert postagem_db.conteudo == "Conteúdo Atualizado", "O conteúdo não foi atualizado"
        assert postagem_db.categoria_artigo.nome == "Comportamento", "A categoria não foi atualizada"

    def test_excluir_postagem_artigo(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        criar_tabela_veterinario()
        criar_tabela()

        conn = get_connection()
        cursor = conn.cursor()

        # Inserir dados necessários
        cursor.execute(
            "INSERT INTO veterinario (id_usuario, nome, email, senha, telefone, crmv, verificado, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (1, "Dr. João", "joao@email.com", "123", "999999999", "CRMV123", True, "Especialista em felinos")
        )
        cursor.execute(
            "INSERT INTO categoria_artigo (id, nome, descricao) VALUES (?, ?, ?)",
            (1, "Saúde", "Descrição")
        )
        conn.commit()
        conn.close()

        # Criar e inserir postagem
        veterinario_teste = Veterinario(1, "Dr. João", "joao@email.com", "123", "999999999", "CRMV123", True, "Especialista em felinos")
        categoria_teste = CategoriaArtigo(1, "Saúde", "Descrição")
        postagem_teste = PostagemArtigo(0, veterinario_teste, "Título", "Conteúdo", categoria_teste, "2025-06-30", 0)
        
        id_postagem = inserir(postagem_teste)

        # Act
        resultado = excluir(id_postagem)

        # Assert
        assert resultado == True, "A exclusão deveria retornar True"
        
        postagem_db = obter_por_id(id_postagem)
        assert postagem_db is None, "A postagem deveria ter sido excluída"

    def test_obter_todos_paginado(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        criar_tabela_veterinario()
        criar_tabela()

        conn = get_connection()
        cursor = conn.cursor()

        # Inserir dados necessários
        cursor.execute(
            "INSERT INTO veterinario (id_usuario, nome, email, senha, telefone, crmv, verificado, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (1, "Dr. João", "joao@email.com", "123", "999999999", "CRMV123", True, "Especialista em felinos")
        )
        cursor.execute(
            "INSERT INTO categoria_artigo (id, nome, descricao) VALUES (?, ?, ?)",
            (1, "Saúde", "Descrição")
        )
        conn.commit()
        conn.close()

        # Criar e inserir múltiplas postagens
        veterinario_teste = Veterinario(1, "Dr. João", "joao@email.com", "123", "999999999", "CRMV123", True, "Especialista em felinos")
        categoria_teste = CategoriaArtigo(1, "Saúde", "Descrição")
        
        for i in range(5):
            postagem = PostagemArtigo(0, veterinario_teste, f"Título {i+1}", f"Conteúdo {i+1}", categoria_teste, "2025-06-30", 0)
            inserir(postagem)

        # Act
        postagens = obter_todos_paginado(limite=3, offset=0)

        # Assert
        assert len(postagens) == 3, "Deveria retornar 3 postagens"
        assert all(isinstance(p, PostagemArtigo) for p in postagens), "Todos os itens deveriam ser PostagemArtigo"