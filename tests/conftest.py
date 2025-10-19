"""
Fixtures compartilhadas para os testes do VetConecta.

Este arquivo contém fixtures que são automaticamente disponibilizadas
para todos os testes do projeto.
"""

import os
import tempfile
import pytest
from datetime import datetime

from model.usuario_model import Usuario
from model.administrador_model import Administrador


@pytest.fixture
def test_db():
    """
    Cria um banco de dados SQLite temporário para testes.

    O banco é criado antes de cada teste e destruído após,
    garantindo isolamento completo entre testes.

    Yields:
        str: Caminho para o arquivo de banco de dados temporário
    """
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.environ["TEST_DATABASE_PATH"] = db_path

    try:
        yield db_path
    finally:
        try:
            os.close(db_fd)
        except OSError:
            pass  # Já foi fechado

        try:
            os.remove(db_path)
        except (PermissionError, FileNotFoundError):
            # Em Windows, o arquivo pode estar bloqueado
            pass


@pytest.fixture
def usuario_padrao():
    """
    Cria uma instância padrão de Usuario para testes.

    Returns:
        Usuario: Objeto Usuario com dados de teste
    """
    return Usuario(
        id_usuario=0,
        nome="João Test",
        email="joao.test@vetconecta.com",
        senha="senha_segura_123",
        telefone="11999999999",
        perfil="tutor",
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
    )


@pytest.fixture
def veterinario_padrao():
    """
    Cria uma instância padrão de Veterinário para testes.

    Returns:
        Usuario: Objeto Usuario com perfil veterinário
    """
    return Usuario(
        id_usuario=0,
        nome="Dra. Maria Veterinária",
        email="maria.vet@vetconecta.com",
        senha="senha_segura_456",
        telefone="11888888888",
        perfil="veterinario",
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
    )


@pytest.fixture
def admin_padrao():
    """
    Cria uma instância padrão de Administrador para testes.

    Returns:
        Administrador: Objeto Administrador com dados de teste
    """
    return Administrador(
        id_admin=0,
        nome="Admin Test",
        email="admin@vetconecta.com",
        senha="admin_senha_789",
    )


@pytest.fixture
def data_atual():
    """
    Retorna a data/hora atual para testes.

    Returns:
        datetime: Data/hora atual
    """
    return datetime.now()


@pytest.fixture
def email_unico():
    """
    Gera um email único para testes usando timestamp.

    Returns:
        function: Função que gera emails únicos
    """
    import time

    def _gerar_email(prefixo="test"):
        timestamp = str(int(time.time() * 1000000))  # microsegundos
        return f"{prefixo}_{timestamp}@test.com"

    return _gerar_email
