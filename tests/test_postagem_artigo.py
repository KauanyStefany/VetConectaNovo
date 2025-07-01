import os
import sys
from data.categoria_artigo_repo import *
from data.categoria_artigo_model import CategoriaArtigo
from data.postagem_artigo_repo import *
from data.postagem_artigo_model import PostagemArtigo
from data.veterinario_repo import *

class TestPostagemArtigoRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_postagem_artigo(self, test_db):
        # Arrange
        criar_tabela_tutor()
        criar_tabela_categoria_artigo()
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
        postagem_teste = postagem = PostagemArtigo(0,Veterinario(id_usuario=1,nome="Dr. João",email="joao@email.com",senha="123",telefone="999999999",crmv="CRMV123",verificado=True,bio="Especialista em felinos"),"Título","Conteúdo",CategoriaArtigo(1, "Saúde","Descrição"),"2025-06-30",0)
        # Act
        id_postagem_criada = inserir(postagem_teste) 
        # Assert
        postagem_db = obter_por_id(id_postagem_criada)
        assert postagem_db is not None, "A postagem retornada não deveria ser None"
        assert postagem_db.id == 1, "O ID da postagem criada deveria ser 1"
        assert postagem_db.titulo == "Título", "O título da postagem não confere"
        assert postagem_db.conteudo == "Conteúdo", "O conteúdo da postagem não confere"
        assert postagem_db.veterinario.nome == "Nome do Veterinário", "O nome do veterinário não confere"
        assert postagem_db.categoria_artigo.nome == "Categoria", "A categoria do artigo não confere"
        assert postagem_db.data_publicacao == "Data", "A data de publicação da postagem não confere"
        assert postagem_db.visualizacoes == 0, "O número de visualizações deveria ser 0"
                