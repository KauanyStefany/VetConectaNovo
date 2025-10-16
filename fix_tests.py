#!/usr/bin/env python3
"""
Script para corrigir automaticamente os testes adicionando os novos campos do Usuario.
"""

import re
import os

# Padrão para encontrar construções do tipo Usuario(...) com menos de 10 argumentos
# O Usuario agora precisa de 10 argumentos

def fix_usuario_constructor(content):
    """Corrige as construções de Usuario para incluir todos os campos obrigatórios."""

    # Padrão 1: Usuario com 5 argumentos posicionais (formato antigo)
    # Usuario(0, "Nome", "email", "senha", "telefone")
    pattern1 = r'Usuario\((\d+),\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\)'
    replacement1 = r'Usuario(\1, "\2", "\3", "\4", "\5", "tutor", None, None, None, None)'
    content = re.sub(pattern1, replacement1, content)

    # Padrão 2: self.usuario = Usuario(...) no setup
    # Já corrigido manualmente, mas garantir

    return content

def process_file(filepath):
    """Processa um arquivo de teste."""
    print(f"Processando: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    content = fix_usuario_constructor(content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Atualizado")
        return True
    else:
        print(f"  - Sem alterações")
        return False

def main():
    """Processa todos os arquivos de teste."""
    tests_dir = "tests"

    if not os.path.exists(tests_dir):
        print(f"Erro: Diretório {tests_dir} não encontrado")
        return

    test_files = [
        "test_verificacao_crmv_repo.py",
        "test_tutor_repo.py",
        "test_veterinario_repo.py",
        "test_administrador_repo.py",
        "test_categoria_artigo_repo.py",
        "test_comentario_repo.py",
        "test_curtida_artigo_repo.py",
        "test_curtida_feed.py",
        "test_postagem_artigo.py",
        "test_postagem_feed.py",
        "test_resposta_chamado.py",
        "test_seguida_repo.py"
    ]

    updated_count = 0
    for test_file in test_files:
        filepath = os.path.join(tests_dir, test_file)
        if os.path.exists(filepath):
            if process_file(filepath):
                updated_count += 1
        else:
            print(f"Aviso: Arquivo não encontrado: {filepath}")

    print(f"\nResumo: {updated_count} arquivos atualizados")

if __name__ == "__main__":
    main()
