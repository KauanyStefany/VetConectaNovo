import os
import sys
from data.postagem_feed_repo import *
from data.postagem_feed_model import PostagemFeed
from data.usuario_model import Usuario
from data import usuario_repo, usuario_sql
from data import tutor_repo
from data import postagem_feed_repo
from data.tutor_model import Tutor


class TestPostagemFeedRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_postagem_feed(self, test_db):
        # Arrange
        # 1. Criar tabelas na ordem correta
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        
        # 2. Criar usuário primeiro
        usuario = Usuario(
            id_usuario=0,
            nome="Tutor Teste",
            email="tutor@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        id_usuario = usuario_repo.inserir_usuario(usuario)
        assert id_usuario is not None, "Falha ao inserir usuário"
        
        # 3. Inserir tutor
        tutor = Tutor(
            id_usuario=id_usuario,
            nome="Tutor Teste",
            email="tutor@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        id_tutor = tutor_repo.inserir_tutor(tutor)
        assert id_tutor is not None, "Falha ao inserir tutor"
        
        # 4. Criar objeto Tutor para a postagem
        tutor_obj = Tutor(
            id=id_tutor,
            nome="Tutor Teste"
        )
        
        # 5. Criar postagem
        postagem_feed_teste = PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_obj,
            imagem="imagem_teste.jpg",
            descricao="Descrição da postagem de teste",
            data_postagem=""
        )
        
        # Act
        id_postagem_inserido = postagem_feed_repo.inserir(postagem_feed_teste)
        
        # Assert
        assert id_postagem_inserido is not None, "A inserção deveria retornar um ID válido"
        
        postagem_db = postagem_feed_repo.obter_por_id(id_postagem_inserido)
        assert postagem_db is not None, "A postagem inserida não deveria ser None"
        assert postagem_db.id_postagem_feed == id_postagem_inserido, "O ID da postagem inserida não confere"
        assert postagem_db.imagem == "imagem_teste.jpg", "A imagem da postagem inserida não confere"
        assert postagem_db.descricao == "Descrição da postagem de teste", "A descrição da postagem inserida não confere"
        assert postagem_db.tutor.id_usuario == id_tutor, "O ID do tutor da postagem inserida não confere"
        assert postagem_db.data_postagem is not None, "A data da postagem não deveria ser None"

    def test_atualizar_postagem_feed(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        
        # Inserir usuário
        usuario_id = usuario_repo.inserir_usuario(Usuario(
            id_usuario=0, 
            nome="Tutor Teste", 
            email="tutor@teste.com", 
            senha="12345678", 
            telefone="11999999999"
        ))
        
        # Inserir tutor
        tutor_id = tutor_repo.inserir_tutor(Tutor(
            id_usuario=usuario_id,
            nome="Tutor Teste",
            email="tutor@teste.com",
            senha="12345678",
            telefone="11999999999"
        ))
        
        # Inserir postagem
        postagem_id = postagem_feed_repo.inserir(PostagemFeed(
            id_postagem_feed=0,
            tutor=Tutor(id=tutor_id, nome="Tutor Teste"),
            imagem="imagem_original.jpg",
            descricao="Descrição original",
            data_postagem=""
        ))
        
        # Atualizar a postagem
        postagem_atualizada = PostagemFeed(
            id_postagem_feed=postagem_id,
            tutor=Tutor(id=tutor_id, nome="Tutor Teste"),
            imagem="imagem_original.jpg",  # Não altera na função atual
            descricao="Descrição atualizada",
            data_postagem=""
        )
        
        # Act
        resultado = postagem_feed_repo.atualizar(postagem_atualizada)
        
        # Assert
        assert resultado == True, "A atualização da postagem deveria retornar True"
        postagem_db = postagem_feed_repo.obter_por_id(postagem_id)
        assert postagem_db is not None, "A postagem atualizada não deveria ser None"
        assert postagem_db.id_postagem_feed == postagem_id, "O ID da postagem atualizada não confere"
        assert postagem_db.tutor.id_usuario == tutor_id, "O ID do tutor da postagem atualizada não confere"
        assert postagem_db.imagem == "imagem_original.jpg", "A imagem da postagem atualizada não confere"
        assert postagem_db.descricao == "Descrição atualizada", "A descrição da postagem atualizada não confere"
        assert postagem_db.data_postagem is not None, "A data da postagem atualizada não deveria ser None"

    def test_excluir_postagem_feed(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        
        # Inserir usuário
        usuario_id = usuario_repo.inserir_usuario(Usuario(
            id_usuario=0, 
            nome="Tutor Teste", 
            email="tutor@teste.com", 
            senha="12345678", 
            telefone="11999999999"
        ))
        
        # Inserir tutor
        tutor_id = tutor_repo.inserir_tutor(Tutor(
            id_usuario=usuario_id,
            nome="Tutor Teste",
            email="tutor@teste.com",
            senha="12345678",
            telefone="11999999999"
        ))
        
        # Inserir postagem
        postagem_id = postagem_feed_repo.inserir(PostagemFeed(
            id_postagem_feed=0,
            tutor=Tutor(id=tutor_id, nome="Tutor Teste"),
            imagem="imagem_teste.jpg",
            descricao="Descrição teste",
            data_postagem=""
        ))
        
        # Act
        resultado = postagem_feed_repo.excluir(postagem_id)
        
        # Assert
        assert resultado == True, "A exclusão da postagem deveria retornar True"
        postagem_db = postagem_feed_repo.obter_por_id(postagem_id)
        assert postagem_db is None, "A postagem excluída deveria ser None"

    def test_obter_todos_paginado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        
        # Inserir usuário
        usuario_id = usuario_repo.inserir_usuario(Usuario(
            id_usuario=0, 
            nome="Tutor Teste", 
            email="tutor@teste.com", 
            senha="12345678", 
            telefone="11999999999"
        ))
        
        # Inserir tutor
        tutor_id = tutor_repo.inserir_tutor(Tutor(
            id_usuario=usuario_id,
            nome="Tutor Teste",
            email="tutor@teste.com",
            senha="12345678",
            telefone="11999999999"
        ))
        
        # Inserir múltiplas postagens
        tutor_obj = Tutor(id=tutor_id, nome="Tutor Teste")
        
        postagem_feed_repo.inserir(PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_obj,
            imagem="imagem1.jpg",
            descricao="Primeira postagem",
            data_postagem=""
        ))
        
        postagem_feed_repo.inserir(PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_obj,
            imagem="imagem2.jpg",
            descricao="Segunda postagem",
            data_postagem=""
        ))
        
        postagem_feed_repo.inserir(PostagemFeed(
            id_postagem_feed=0,
            tutor=tutor_obj,
            imagem="imagem3.jpg",
            descricao="Terceira postagem",
            data_postagem=""
        ))
        
        # Act
        postagens = postagem_feed_repo.obter_todos_paginado(limite=2, offset=0)
        
        # Assert
        assert len(postagens) == 2, "Deveria retornar 2 postagens"
        assert all(isinstance(p, PostagemFeed) for p in postagens), "Todos os itens deveriam ser PostagemFeed"
        assert all(p.tutor.nome == "Tutor Teste" for p in postagens), "Todas as postagens deveriam ter o tutor correto"
        
        # Verifica ordenação por data (mais recente primeiro)
        descricoes = [p.descricao for p in postagens]
        assert "Terceira postagem" in descricoes, "Terceira postagem deveria estar nos resultados"
        assert "Segunda postagem" in descricoes, "Segunda postagem deveria estar nos resultados"

    def test_obter_por_id(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        tutor_repo.criar_tabela_tutor()
        postagem_feed_repo.criar_tabela()
        
        # Inserir usuário
        usuario_id = usuario_repo.inserir_usuario(Usuario(
            id_usuario=0, 
            nome="Tutor Teste", 
            email="tutor@teste.com", 
            senha="12345678", 
            telefone="11999999999"
        ))
        
        # Inserir tutor
        tutor_id = tutor_repo.inserir_tutor(Tutor(
            id_usuario=usuario_id,
            nome="Tutor Teste",
            email="tutor@teste.com",
            senha="12345678",
            telefone="11999999999"
        ))
        
        # Inserir postagem
        postagem_id = postagem_feed_repo.inserir(PostagemFeed(
            id_postagem_feed=0,
            tutor=Tutor(id=tutor_id, nome="Tutor Teste"),
            imagem="imagem_teste.jpg",
            descricao="Descrição teste",
            data_postagem=""
        ))
        
        # Act
        postagem_obtida = postagem_feed_repo.obter_por_id(postagem_id)
        
        # Assert
        assert postagem_obtida is not None, "A postagem obtida não deveria ser None"
        assert postagem_obtida.id_postagem_feed == postagem_id, "O ID da postagem obtida não confere"
        assert postagem_obtida.tutor.id == tutor_id, "O ID do tutor da postagem obtida não confere"
        assert postagem_obtida.tutor.nome == "Tutor Teste", "O nome do tutor da postagem obtida não confere"
        assert postagem_obtida.imagem == "imagem_teste.jpg", "A imagem da postagem obtida não confere"
        assert postagem_obtida.descricao == "Descrição teste", "A descrição da postagem obtida não confere"
        assert postagem_obtida.data_postagem is not None, "A data da postagem obtida não deveria ser None"

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        postagem_feed_repo.criar_tabela()
        
        # Act
        postagem_obtida = postagem_feed_repo.obter_por_id(999)
        
        # Assert
        assert postagem_obtida is None, "Deveria retornar None para ID inexistente"