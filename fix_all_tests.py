#!/usr/bin/env python3
"""
Script para corrigir TODOS os testes automaticamente.
Corrige Tutor (12 campos) e Veterinario (13 campos).
"""

import re
from pathlib import Path

def fix_tutor_multiline(content):
    """Corrige construções multilinhas de Tutor."""
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detectar início de construção Tutor
        if 'Tutor(' in line and 'quantidade_pets' in content[content.find(line):content.find(line)+500]:
            # Verificar se já tem perfil
            chunk = '\n'.join(lines[i:min(i+20, len(lines))])
            if 'perfil=' not in chunk and 'perfil =' not in chunk:
                # Precisa adicionar campos de Usuario
                result.append(line)
                i += 1

                # Encontrar onde inserir (após telefone, antes de quantidade_pets)
                while i < len(lines) and 'quantidade_pets' not in lines[i]:
                    result.append(lines[i])
                    if 'telefone=' in lines[i] or 'telefone =' in lines[i]:
                        # Inserir campos após telefone
                        result.append('            perfil="tutor",')
                        result.append('            foto=None,')
                        result.append('            token_redefinicao=None,')
                        result.append('            data_token=None,')
                        result.append('            data_cadastro=None,')
                    i += 1
                continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def fix_tutor_inline(content):
    """Corrige construções inline de Tutor com 7 argumentos."""
    # Padrão: Tutor(id, "nome", "email", "senha", "tel", qtd, "desc")
    pattern = r'Tutor\((\d+),\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*(\d+),\s*("([^"]*)"|None)\)'

    def replacer(match):
        return f'Tutor({match.group(1)}, "{match.group(2)}", "{match.group(3)}", "{match.group(4)}", "{match.group(5)}", "tutor", None, None, None, None, {match.group(6)}, {match.group(7)})'

    return re.sub(pattern, replacer, content)


def fix_veterinario_multiline(content):
    """Corrige construções multilinhas de Veterinario."""
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detectar início de construção Veterinario
        if 'Veterinario(' in line or 'veterinario =' in line.lower():
            # Verificar se já tem perfil
            chunk = '\n'.join(lines[i:min(i+20, len(lines))])
            if 'perfil=' not in chunk and 'perfil =' not in chunk and 'crmv' in chunk:
                # Precisa adicionar campos de Usuario
                result.append(line)
                i += 1

                # Encontrar onde inserir (após telefone, antes de crmv)
                while i < len(lines) and 'crmv' not in lines[i].lower():
                    result.append(lines[i])
                    if 'telefone=' in lines[i] or 'telefone =' in lines[i]:
                        # Inserir campos após telefone
                        result.append('            perfil="veterinario",')
                        result.append('            foto=None,')
                        result.append('            token_redefinicao=None,')
                        result.append('            data_token=None,')
                        result.append('            data_cadastro=None,')
                    i += 1
                continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def fix_file(filepath):
    """Corrige um arquivo de teste."""
    print(f"\nProcessando: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Aplicar correções
    if 'Tutor' in content:
        content = fix_tutor_inline(content)
        content = fix_tutor_multiline(content)

    if 'Veterinario' in content:
        content = fix_veterinario_multiline(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Atualizado!")
        return True
    else:
        print(f"  ℹ️  Nenhuma alteração necessária")
        return False


def main():
    """Processa todos os arquivos de teste."""
    test_dir = Path('tests')

    test_files = [
        'test_tutor_repo.py',
        'test_veterinario_repo.py',
    ]

    updated = 0
    for filename in test_files:
        filepath = test_dir / filename
        if filepath.exists():
            if fix_file(filepath):
                updated += 1
        else:
            print(f"⚠️  Arquivo não encontrado: {filepath}")

    print(f"\n{'='*50}")
    print(f"Resumo: {updated} arquivo(s) atualizado(s)")
    print(f"{'='*50}\n")


if __name__ == '__main__':
    main()
