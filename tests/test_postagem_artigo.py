from datetime import datetime
import os
import sys
from data import usuario_repo, veterinario_repo, categoria_artigo_repo, postagem_artigo_repo
from data.categoria_artigo_model import CategoriaArtigo
from data.postagem_artigo_model import PostagemArtigo
from data.veterinario_model import Veterinario
from util import get_connection

class TestPostagemArtigoRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = postagem_artigo_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_postagem_artigo(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        veterinario_repo.criar_tabela_veterinario()
        categoria_artigo_repo.criar_tabela_categoria_artigo()
        postagem_artigo_repo.criar_tabela()

        vet = Veterinario(
            id_usuario=0, 
            nome="Dr. João", 
            email="joao@email.com",
            senha="123", 
            telefone="999999999", 
            crmv="CRMV123", 
            verificado=True, 
            bio="Especialista em felinos")
        id_vet = veterinario_repo.inserir_veterinario(vet)

        categoria = CategoriaArtigo(id=0, nome="Saúde Felina", descricao="Cuidados com gatos")
        id_cat = categoria_artigo_repo.inserir_categoria(categoria)

        postagem = PostagemArtigo(
            id=0,
            id_veterinario=id_vet,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_cat,
            data_publicacao=datetime.today().date(),
            visualizacoes=0
        )
        # Act
        id_post = postagem_artigo_repo.inserir(postagem)
        # Assert
        assert id_post is not None, "A inserção deveria retornar um ID válido"
        postagem_db = postagem_artigo_repo.obter_por_id(id_post)
        assert postagem_db is not None, "A postagem deveria ser inserida e recuperada"
        assert postagem_db.titulo == postagem.titulo, "O título da postagem recuperada está incorreto"
        assert postagem_db.conteudo == postagem.conteudo, "O conteúdo da postagem recuperada está incorreto"
        assert postagem_db.id_categoria_artigo == postagem.id_categoria_artigo, "A categoria da postagem recuperada está incorreta"
        assert postagem_db.data_publicacao == postagem.data_publicacao, "A data de publicação da postagem recuperada está incorreta"
        assert postagem_db.visualizacoes == postagem.visualizacoes, "As visualizações da postagem recuperada estão incorretas"

    def test_obter_por_id(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        veterinario_repo.criar_tabela_veterinario()
        categoria_artigo_repo.criar_tabela_categoria_artigo()
        postagem_artigo_repo.criar_tabela()

        vet = Veterinario(
            id_usuario=0, 
            nome="Dr. João", 
            email="joao@email.com",
            senha="123", 
            telefone="999999999", 
            crmv="CRMV123", 
            verificado=True, 
            bio="Especialista em felinos")
        id_vet = veterinario_repo.inserir_veterinario(vet)

        categoria = CategoriaArtigo(id=0, nome="Saúde Felina", descricao="Cuidados com gatos")
        id_cat = categoria_artigo_repo.inserir_categoria(categoria)

        postagem = PostagemArtigo(
            id=0,
            id_veterinario=id_vet,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_cat,
            data_publicacao=datetime.today().date(),
            visualizacoes=0
        )
        id_post = postagem_artigo_repo.inserir(postagem) 
        # Act
        postagem_db = postagem_artigo_repo.obter_por_id(id_post)
        # Assert
        assert postagem_db is not None, "A postagem deveria ser inserida e recuperada"
        assert postagem_db.titulo == postagem.titulo, "O título da postagem recuperada está incorreto"
        assert postagem_db.conteudo == postagem.conteudo, "O conteúdo da postagem recuperada está incorreto"
        assert postagem_db.id_categoria_artigo == postagem.id_categoria_artigo, "A categoria da postagem recuperada está incorreta"
        assert postagem_db.data_publicacao == postagem.data_publicacao, "A data de publicação da postagem recuperada está incorreta"
        assert postagem_db.visualizacoes == postagem.visualizacoes, "As visualizações da postagem recuperada estão incorretas"
    
    def test_atualizar_postagem_artigo(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        veterinario_repo.criar_tabela_veterinario()
        categoria_artigo_repo.criar_tabela_categoria_artigo()
        postagem_artigo_repo.criar_tabela()
        vet = Veterinario(
            id_usuario=0, 
            nome="Dr. João", 
            email="joao@email.com",
            senha="123", 
            telefone="999999999", 
            crmv="CRMV123", 
            verificado=True, 
            bio="Especialista em felinos")
        id_vet = veterinario_repo.inserir_veterinario(vet)
        categoria = CategoriaArtigo(id=0, nome="Saúde Felina", descricao="Cuidados com gatos")
        id_cat = categoria_artigo_repo.inserir_categoria(categoria)
        postagem = PostagemArtigo(
            id=0,
            id_veterinario=id_vet,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_cat,
            data_publicacao=datetime.today().date(),
            visualizacoes=0
        )        
        id_post = postagem_artigo_repo.inserir(postagem)                
        postagem_db = postagem_artigo_repo.obter_por_id(id_post)
        # Act
        postagem_db.titulo = "Vacinação de Gatos Atualizado"
        postagem_db.conteudo = "Texto do artigo atualizado"
        postagem_artigo_repo.atualizar(postagem_db)
        # Assert
        postagem_atualizada = postagem_artigo_repo.obter_por_id(id_post)
        assert postagem_atualizada is not None, "A postagem deveria ser inserida e recuperada"
        assert postagem_atualizada.titulo == "Vacinação de Gatos Atualizado", "O título da postagem atualizada está incorreto"
        assert postagem_atualizada.conteudo == "Texto do artigo atualizado", "O conteúdo da postagem atualizada está incorreto"
        assert postagem_atualizada.id_categoria_artigo == id_cat, "A categoria da postagem atualizada está incorreta"
        assert postagem_atualizada.data_publicacao == datetime.today().date(), "A data de publicação da postagem atualizada está incorreta"
        assert postagem_atualizada.visualizacoes == 0, "As visualizações da postagem atualizada estão incorretas"

    def test_excluir_postagem_artigo(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        veterinario_repo.criar_tabela_veterinario()
        categoria_artigo_repo.criar_tabela_categoria_artigo()
        postagem_artigo_repo.criar_tabela()
        vet = Veterinario(
            id_usuario=0, 
            nome="Dr. João", 
            email="joao@email.com",
            senha="123", 
            telefone="999999999", 
            crmv="CRMV123", 
            verificado=True, 
            bio="Especialista em felinos")
        id_vet = veterinario_repo.inserir_veterinario(vet)
        categoria = CategoriaArtigo(id=0, nome="Saúde Felina", descricao="Cuidados com gatos")
        id_cat = categoria_artigo_repo.inserir_categoria(categoria)
        postagem = PostagemArtigo(
            id=0,
            id_veterinario=id_vet,
            titulo="Vacinação de Gatos",
            conteudo="Texto do artigo",
            id_categoria_artigo=id_cat,
            data_publicacao=datetime.today().date(),
            visualizacoes=0
        )        
        id_post = postagem_artigo_repo.inserir(postagem)                
        postagem_db = postagem_artigo_repo.obter_por_id(id_post)
        # Act
        excluiu = postagem_artigo_repo.excluir(id_post)
        # Assert
        assert excluiu is True, "A exclusão deveria retornar True"
        postagem_excluida = postagem_artigo_repo.obter_por_id(id_post)
        assert postagem_excluida is None, "A postagem deveria ser excluída e não recuperada"
        

    def test_obter_todos_paginado(self, test_db):
       # Arrange
        usuario_repo.criar_tabela_usuario()
        veterinario_repo.criar_tabela_veterinario()
        categoria_artigo_repo.criar_tabela_categoria_artigo()
        postagem_artigo_repo.criar_tabela()
        vet = Veterinario(
            id_usuario=0, 
            nome="Dr. João", 
            email="joao@email.com",
            senha="123", 
            telefone="999999999", 
            crmv="CRMV123", 
            verificado=True, 
            bio="Especialista em felinos")
        id_vet = veterinario_repo.inserir_veterinario(vet)
        categoria = CategoriaArtigo(id=0, nome="Saúde Felina", descricao="Cuidados com gatos")
        id_cat = categoria_artigo_repo.inserir_categoria(categoria)
        ids_posts = []
        for i in range(10):
            postagem = PostagemArtigo(
                id=0,
                id_veterinario=id_vet,
                titulo=f"Vacinação de Gatos {i}",
                conteudo=f"Texto do artigo {i}",
                id_categoria_artigo=id_cat,
                data_publicacao=datetime.today().date(),
                visualizacoes=i*10
            )        
            id_post = postagem_artigo_repo.inserir(postagem)
            ids_posts.append(id_post)
        # Act
        pagina1 = postagem_artigo_repo.obter_todos_paginado(1, 6)
        pagina2 = postagem_artigo_repo.obter_todos_paginado(2, 6)
        # Assert
        assert len(pagina1) == 6, "A primeira página deveria conter 6 postagens"
        assert len(pagina2) == 4, "A segunda página deveria conter 4 postagens"
        assert pagina1[0].id == ids_posts[0], "A primeira postagem da primeira página está incorreta"
        assert pagina2[0].id == ids_posts[6], "A primeira postagem da segunda página está incorreta"
        