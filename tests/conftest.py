# import pytest
# import os
# import sys
# import tempfile


# # Adiciona o diretório raiz do projeto ao PYTHONPATH
# # Isso permite importar módulos do projeto nos testes
# project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, project_root)

# # Fixture para criar um banco de dados temporário para testes
# @pytest.fixture
# def test_db():
#     # Cria um arquivo temporário para o banco de dados
#     db_fd, db_path = tempfile.mkstemp(suffix='.db')
#     # Configura a variável de ambiente para usar o banco de teste
#     os.environ['TEST_DATABASE_PATH'] = db_path
#     # Retorna o caminho do banco de dados temporário
#     yield db_path    
#     # Remove o arquivo temporário ao concluir o teste
#     os.close(db_fd)
#     if os.path.exists(db_path):
#         os.unlink(db_path)


import os
import tempfile
import pytest

@pytest.fixture
def test_db():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['TEST_DATABASE_PATH'] = db_path
    try:
        yield db_path
    finally:
        try:
            os.close(db_fd)
        except:
            pass  # já pode estar fechado

        try:
            os.remove(db_path)
        except PermissionError:
            print(f"[WARN] Banco ainda em uso: {db_path}")
