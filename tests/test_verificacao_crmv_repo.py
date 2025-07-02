import os
import sys
from data.administrador_repo import criar_tabela_administrador
from data.verificacao_crmv_model import VerificacaoCRMV
from data.verificacao_crmv_repo import *
from data.veterinario_repo import criar_tabela_veterinario
class TestVerificacaoCRMVRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela de verificações de CRMV deveria retornar True"

    



    