#!/usr/bin/env python3
"""
Script para corrigir os testes restantes com problemas de assinatura.
Corrige Usuario (10 campos), Tutor (12 campos), e Veterinario (13 campos).
"""

import re
from pathlib import Path


def fix_usuario_patterns(content):
    """Corrige padrões de Usuario com 5 campos para 10 campos."""
    # Padrão: Usuario(id, "nome", "email", "senha", "telefone")
    pattern = r'Usuario\(\s*(\d+),\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\s*\)'

    def replacer(match):
        return f'Usuario({match.group(1)}, "{match.group(2)}", "{match.group(3)}", "{match.group(4)}", "{match.group(5)}", "tutor", None, None, None, None)'

    return re.sub(pattern, replacer, content)


def fix_tutor_inline_7params(content):
    """Corrige Tutor inline com 7 parâmetros para 12."""
    # Padrão: Tutor(id, "nome", "email", "senha", "tel", qtd, desc)
    pattern = r'Tutor\(\s*(\d+),\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*(\d+),\s*((?:"[^"]*"|None))\s*\)'

    def replacer(match):
        return f'Tutor({match.group(1)}, "{match.group(2)}", "{match.group(3)}", "{match.group(4)}", "{match.group(5)}", "tutor", None, None, None, None, {match.group(6)}, {match.group(7)})'

    return re.sub(pattern, replacer, content)


def fix_veterinario_inline_8params(content):
    """Corrige Veterinario inline com 8 parâmetros para 13."""
    # Padrão: Veterinario(id, "nome", "email", "senha", "tel", "crmv", verificado, "bio")
    pattern = r'Veterinario\(\s*(\d+),\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*(True|False),\s*((?:"[^"]*"|None))\s*\)'

    def replacer(match):
        return f'Veterinario({match.group(1)}, "{match.group(2)}", "{match.group(3)}", "{match.group(4)}", "{match.group(5)}", "veterinario", None, None, None, None, "{match.group(6)}", {match.group(7)}, {match.group(8)})'

    return re.sub(pattern, replacer, content)


def fix_multiline_usuario(content):
    """Corrige construções multilinhas de Usuario."""
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detectar Usuario( sem perfil nos próximos 15 linhas
        if 'Usuario(' in line and 'Usuario.__init__' not in line:
            # Verificar se já tem perfil
            chunk = '\n'.join(lines[i:min(i+20, len(lines))])
            if 'perfil=' not in chunk and 'perfil =' not in chunk:
                # Precisa adicionar campos
                result.append(line)
                i += 1

                # Encontrar onde inserir (após telefone)
                while i < len(lines):
                    current_line = lines[i]
                    result.append(current_line)

                    # Verifica se chegou no fim do construtor Usuario
                    if ')' in current_line and 'telefone' in '\n'.join(result[-5:]):
                        # Inserir antes do )
                        if current_line.strip() == ')':
                            # Inserir campos antes do )
                            result.pop()  # Remove o )
                            result.append('            perfil="tutor",')
                            result.append('            foto=None,')
                            result.append('            token_redefinicao=None,')
                            result.append('            data_token=None,')
                            result.append('            data_cadastro=None')
                            result.append(current_line)  # Re-adiciona o )
                        break
                    i += 1
                continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def fix_multiline_veterinario(content):
    """Corrige construções multilinhas de Veterinario."""
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detectar Veterinario( ou vet = Veterinario(
        if ('Veterinario(' in line or 'veterinario = Veterinario(' in line.lower()) and 'Veterinario.__init__' not in line:
            # Verificar se já tem perfil
            chunk = '\n'.join(lines[i:min(i+25, len(lines))])
            if 'perfil=' not in chunk and 'perfil =' not in chunk and ('crmv' in chunk or 'verificado' in chunk):
                # Precisa adicionar campos de Usuario
                result.append(line)
                i += 1

                # Encontrar onde inserir (após telefone, antes de crmv)
                found_telefone = False
                while i < len(lines) and 'crmv' not in lines[i].lower():
                    current_line = lines[i]
                    result.append(current_line)
                    if 'telefone=' in current_line or 'telefone =' in current_line:
                        found_telefone = True
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


def fix_multiline_tutor(content):
    """Corrige construções multilinhas de Tutor."""
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detectar Tutor(
        if ('Tutor(' in line or 'tutor = Tutor(' in line.lower()) and 'Tutor.__init__' not in line:
            # Verificar se já tem perfil
            chunk = '\n'.join(lines[i:min(i+25, len(lines))])
            if 'perfil=' not in chunk and 'perfil =' not in chunk and ('quantidade_pets' in chunk or 'descricao_pets' in chunk):
                # Precisa adicionar campos de Usuario
                result.append(line)
                i += 1

                # Encontrar onde inserir (após telefone, antes de quantidade_pets)
                while i < len(lines) and 'quantidade_pets' not in lines[i].lower():
                    current_line = lines[i]
                    result.append(current_line)
                    if 'telefone=' in current_line or 'telefone =' in current_line:
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


def fix_file(filepath):
    """Corrige um arquivo de teste."""
    print(f"\nProcessando: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Aplicar correções inline primeiro
    content = fix_usuario_patterns(content)
    content = fix_tutor_inline_7params(content)
    content = fix_veterinario_inline_8params(content)

    # Depois correções multilinhas
    if 'Usuario(' in content:
        content = fix_multiline_usuario(content)

    if 'Tutor' in content:
        content = fix_multiline_tutor(content)

    if 'Veterinario' in content:
        content = fix_multiline_veterinario(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Atualizado!")
        return True
    else:
        print(f"  ℹ️  Nenhuma alteração necessária")
        return False


def main():
    """Processa todos os arquivos de teste que ainda têm problemas."""
    test_dir = Path('tests')

    # Lista de arquivos com problemas identificados
    test_files = [
        'test_comentario_repo.py',
        'test_curtida_artigo_repo.py',
        'test_curtida_feed.py',
        'test_postagem_artigo.py',
        'test_postagem_feed.py',
        'test_resposta_chamado.py',
        'test_seguida_repo.py',
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
