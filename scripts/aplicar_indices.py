#!/usr/bin/env python3
"""
Script para aplicar índices no banco de dados.
Este script lê o arquivo sql/indices.sql e aplica todos os índices no banco.
"""

import sqlite3
import os
import sys

# Adiciona o diretório pai ao path para importar módulos do projeto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.db_util import get_connection


def aplicar_indices():
    """Aplica todos os índices definidos em sql/indices.sql"""
    print("Iniciando aplicação de índices...")

    # Ler arquivo SQL
    sql_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'sql',
        'indices.sql'
    )

    if not os.path.exists(sql_file):
        print(f"Erro: Arquivo {sql_file} não encontrado!")
        return False

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Separar comandos SQL (cada CREATE INDEX é um comando)
    # Remover comentários e separar por linhas
    linhas = sql_content.split('\n')
    comandos = []
    comando_atual = []

    for linha in linhas:
        linha = linha.strip()
        # Pular linhas vazias e comentários
        if not linha or linha.startswith('--'):
            continue

        # Adicionar linha ao comando atual
        comando_atual.append(linha)

        # Se a linha termina com ;, é o fim do comando
        if linha.endswith(';'):
            comando_completo = ' '.join(comando_atual)
            if comando_completo.startswith('CREATE INDEX'):
                comandos.append(comando_completo)
            comando_atual = []

    print(f"Encontrados {len(comandos)} comandos de criação de índices")

    # Aplicar índices
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            indices_criados = 0
            indices_existentes = 0

            for i, comando in enumerate(comandos, 1):
                try:
                    # Extrair nome do índice para feedback
                    partes = comando.split()
                    if 'EXISTS' in comando:
                        idx_pos = partes.index('EXISTS') + 1
                    else:
                        idx_pos = partes.index('INDEX') + 1

                    nome_indice = partes[idx_pos]

                    cursor.execute(comando)

                    if cursor.rowcount == 0:
                        print(f"  [{i}/{len(comandos)}] Índice {nome_indice} já existe")
                        indices_existentes += 1
                    else:
                        print(f"  [{i}/{len(comandos)}] Índice {nome_indice} criado com sucesso")
                        indices_criados += 1

                except sqlite3.Error as e:
                    print(f"  Erro ao criar índice: {e}")
                    continue

            print(f"\n✓ Processo concluído:")
            print(f"  - Índices criados: {indices_criados}")
            print(f"  - Índices já existentes: {indices_existentes}")
            print(f"  - Total: {indices_criados + indices_existentes}")

            return True

    except Exception as e:
        print(f"Erro ao aplicar índices: {e}")
        return False


if __name__ == "__main__":
    sucesso = aplicar_indices()
    sys.exit(0 if sucesso else 1)
