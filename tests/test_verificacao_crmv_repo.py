import os
import sys
from data.verificacao_crmv_model import VerificacaoCRMV
from data.verificacao_crmv_repo import *
class TestVerificacaoCRMVRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela de verificações de CRMV deveria retornar True"

    def test_inserir_verificacao_crmv(self, test_db):
        # Arrange
        criar_tabela()
        nova_verificacao = VerificacaoCRMV(
            id_veterinario=1,
            crmv="SP-123456",
            status="pendente",
            data_solicitacao="2023-10-01"
        )
        # Act
        id_nova_verificacao = inserir(nova_verificacao)
        # Assert
        assert id_nova_verificacao is not None, "A inserção da verificação de CRMV deveria retornar um ID válido"
        verificacao_db = obter_por_id(id_nova_verificacao)
        assert verificacao_db is not None, "A verificação de CRMV inserida não deveria ser None"
        assert verificacao_db.id_veterinario == 1, "O ID do veterinário na verificação inserida não confere"
        assert verificacao_db.crmv == "SP-123456", "O CRMV na verificação inserida não confere"
        assert verificacao_db.status == "pendente", "O status da verificação inserida não confere"
        assert verificacao_db.data_solicitacao == "2023-10-01", "A data de solicitação da verificação inserida não confere"
    