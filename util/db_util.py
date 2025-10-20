import sqlite3
import os
import json
from contextlib import contextmanager
from typing import Generator
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Timeout padrão
DB_TIMEOUT: float = float(os.getenv("DATABASE_TIMEOUT", "30.0"))


# Função para obter o caminho do banco de dados, considerando variáveis
# de ambiente que indicam caminhos diferentes para testes e produção.
def _get_db_path() -> str:
    """Retorna o caminho do banco, lendo variáveis de ambiente dinamicamente."""
    return os.getenv("TEST_DATABASE_PATH") or os.getenv("DATABASE_PATH") or "dados.db"


def _criar_conexao() -> sqlite3.Connection:
    """Cria uma conexão configurada com o banco de dados."""
    try:
        db_path = _get_db_path()  # Lê dinamicamente a cada conexão
        conn = sqlite3.connect(db_path, timeout=DB_TIMEOUT, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        # CRITICAL: Habilitar foreign keys no SQLite
        conn.execute("PRAGMA foreign_keys = ON")
        # Performance improvements
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        raise


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager para gerenciar conexões com commit/rollback automático."""
    conn = _criar_conexao()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro na transação, rollback executado: {e}")
        raise
    finally:
        conn.close()


def get_connection_sem_commit() -> sqlite3.Connection:
    """Retorna conexão sem commit automático para operações de leitura."""
    return _criar_conexao()


def inicializar_banco():
    # Chama o método criar_tabela de cada repositório para garantir que as tabelas existam
    from repo import (
        administrador_repo,
        tutor_repo,
        usuario_repo,
        veterinario_repo,
        categoria_artigo_repo,
        postagem_artigo_repo,
        curtida_artigo_repo,
        postagem_feed_repo,
        curtida_feed_repo,
        denuncia_repo,
        verificacao_crmv_repo,
        seguida_repo,
    )

    usuario_repo.criar_tabela()
    tutor_repo.criar_tabela()
    veterinario_repo.criar_tabela()
    administrador_repo.criar_tabela()
    categoria_artigo_repo.criar_tabela()
    postagem_artigo_repo.criar_tabela()
    curtida_artigo_repo.criar_tabela()
    postagem_feed_repo.criar_tabela()
    curtida_feed_repo.criar_tabela()
    denuncia_repo.criar_tabela()
    verificacao_crmv_repo.criar_tabela()
    seguida_repo.criar_tabela()

    # Importar dados iniciais se necessário
    importar_admins()
    importar_veterinarios()
    importar_tutores()
    importar_categorias_artigos()
    importar_postagens_artigos()
    importar_postagens_feeds()


def importar_admins():
    """Importa administradores do arquivo JSON se a tabela estiver vazia."""
    from repo import administrador_repo
    from model.administrador_model import Administrador
    from util.security import criar_hash_senha

    # Verifica se a tabela está vazia
    admins_existentes = administrador_repo.obter_pagina(offset=0, limite=1)
    if admins_existentes:
        logger.info("Tabela de administradores já contém dados. Importação ignorada.")
        return

    # Lê o arquivo JSON
    json_path = Path(__file__).parent.parent / "data" / "admins.json"
    if not json_path.exists():
        logger.warning(f"Arquivo {json_path} não encontrado.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Importa cada administrador
    for item in dados:
        admin = Administrador(
            id_admin=item["id_admin"],
            nome=item["nome"],
            email=item["email"],
            senha=criar_hash_senha(item["senha"]),
        )
        administrador_repo.importar(admin)
        logger.info(f"Administrador '{admin.nome}' importado com sucesso.")


def importar_tutores():
    """Importa tutores do arquivo JSON se a tabela estiver vazia."""
    from repo import tutor_repo
    from model.tutor_model import Tutor
    from util.security import criar_hash_senha

    # Verifica se a tabela está vazia
    tutores_existentes = tutor_repo.obter_pagina(limite=1, offset=0)
    if tutores_existentes:
        logger.info("Tabela de tutores já contém dados. Importação ignorada.")
        return

    # Lê o arquivo JSON
    json_path = Path(__file__).parent.parent / "data" / "tutores.json"
    if not json_path.exists():
        logger.warning(f"Arquivo {json_path} não encontrado.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Importa cada tutor
    for item in dados:
        tutor = Tutor(
            id_usuario=item["id_usuario"],
            nome=item["nome"],
            email=item["email"],
            senha=criar_hash_senha(item["senha"]),
            telefone=item["telefone"],
            perfil="tutor",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            quantidade_pets=item["quantidade_pets"],
            descricao_pets=item["descricao_pets"],
        )
        tutor_repo.importar(tutor)
        logger.info(f"Tutor '{tutor.nome}' importado com sucesso.")


def importar_veterinarios():
    """Importa veterinários do arquivo JSON se a tabela estiver vazia."""
    from repo import veterinario_repo
    from model.veterinario_model import Veterinario
    from util.security import criar_hash_senha

    # Verifica se a tabela está vazia
    vets_existentes = veterinario_repo.obter_pagina(limite=1, offset=0)
    if vets_existentes:
        logger.info("Tabela de veterinários já contém dados. Importação ignorada.")
        return

    # Lê o arquivo JSON
    json_path = Path(__file__).parent.parent / "data" / "veterinarios.json"
    if not json_path.exists():
        logger.warning(f"Arquivo {json_path} não encontrado.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Importa cada veterinário
    for item in dados:
        vet = Veterinario(
            id_usuario=item["id_usuario"],
            nome=item["nome"],
            email=item["email"],
            senha=criar_hash_senha(item["senha"]),
            telefone=item["telefone"],
            perfil="veterinario",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crmv=item["crmv"],
            verificado=item["verificado"],
            bio=item["bio"],
        )
        veterinario_repo.importar(vet)
        logger.info(f"Veterinário '{vet.nome}' importado com sucesso.")


def importar_categorias_artigos():
    """Importa categorias de artigos do arquivo JSON se a tabela estiver vazia."""
    from repo import categoria_artigo_repo
    from model.categoria_artigo_model import CategoriaArtigo

    # Verifica se a tabela está vazia
    categorias_existentes = categoria_artigo_repo.obter_pagina(offset=0, limite=1)
    if categorias_existentes:
        logger.info("Tabela de categorias de artigos já contém dados. Importação ignorada.")
        return

    # Lê o arquivo JSON
    json_path = Path(__file__).parent.parent / "data" / "categorias_artigos.json"
    if not json_path.exists():
        logger.warning(f"Arquivo {json_path} não encontrado.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Importa cada categoria
    for item in dados:
        categoria = CategoriaArtigo(
            id_categoria_artigo=item["id_categoria_artigo"],
            nome=item["nome"],
            cor=item["cor"],
        )
        categoria_artigo_repo.importar(categoria)
        logger.info(f"Categoria '{categoria.nome}' importada com sucesso.")


def importar_postagens_artigos():
    """Importa postagens de artigos do arquivo JSON se a tabela estiver vazia."""
    from datetime import date
    from repo import postagem_artigo_repo
    from model.postagem_artigo_model import PostagemArtigo

    # Verifica se a tabela está vazia
    postagens_existentes = postagem_artigo_repo.obter_pagina(pagina=1, tamanho_pagina=1)
    if postagens_existentes:
        logger.info("Tabela de postagens de artigos já contém dados. Importação ignorada.")
        return

    # Lê o arquivo JSON
    json_path = Path(__file__).parent.parent / "data" / "postagens_artigos.json"
    if not json_path.exists():
        logger.warning(f"Arquivo {json_path} não encontrado.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Importa cada postagem
    for item in dados:
        postagem = PostagemArtigo(
            id_postagem_artigo=item["id_postagem_artigo"],
            id_veterinario=item["id_veterinario"],
            titulo=item["titulo"],
            conteudo=item["conteudo"],
            id_categoria_artigo=item["id_categoria_artigo"],
            data_publicacao=date.today(),  # Usa data atual pois não está no JSON
            visualizacoes=item.get("visualizacoes", 0),  # Usa 0 como padrão se não existir
        )
        postagem_artigo_repo.importar(postagem)
        logger.info(f"Postagem '{postagem.titulo}' importada com sucesso.")


def importar_postagens_feeds():
    """Importa postagens de feeds do arquivo JSON se a tabela estiver vazia."""
    from datetime import datetime
    from repo import postagem_feed_repo
    from model.postagem_feed_model import PostagemFeed

    # Verifica se a tabela está vazia
    postagens_existentes = postagem_feed_repo.obter_pagina(pagina=1, tamanho_pagina=1)
    if postagens_existentes:
        logger.info("Tabela de postagens de feeds já contém dados. Importação ignorada.")
        return

    # Lê o arquivo JSON
    json_path = Path(__file__).parent.parent / "data" / "postagens_feeds.json"
    if not json_path.exists():
        logger.warning(f"Arquivo {json_path} não encontrado.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Importa cada postagem
    for item in dados:
        postagem = PostagemFeed(
            id_postagem_feed=item["id_postagem_feed"],
            id_tutor=item["id_tutor"],
            descricao=item["descricao"],
            data_postagem=datetime.strptime(item["data_postagem"], "%Y-%m-%d %H:%M:%S").date(),
            visualizacoes=item.get("visualizacoes", 0),
        )
        postagem_feed_repo.importar(postagem)
        logger.info(f"Postagem feed #{postagem.id_postagem_feed} do tutor {postagem.id_tutor} importada com sucesso.")