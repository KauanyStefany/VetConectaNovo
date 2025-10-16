#!/usr/bin/env python3
"""
Script avançado para corrigir testes com Tutor e Veterinario.
"""

import re

def fix_tutor_constructors(content):
    """Corrige construções de Tutor para incluir campos de Usuario."""
    # Pattern: Tutor(id, "nome", "email", "senha", "telefone", qtd_pets, "desc_pets")
    # Pattern com 7 argumentos positivos (formato antigo de Tutor)
    pattern = r'Tutor\((\d+),\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*(\d+|None),\s*("([^"]*)"|None)\)'

    def replacer(match):
        id_usuario = match.group(1)
        nome = match.group(2)
        email = match.group(3)
        senha = match.group(4)
        telefone = match.group(5)
        qtd_pets = match.group(6)
        desc_pets = match.group(7)

        return f'Tutor({id_usuario}, "{nome}", "{email}", "{senha}", "{telefone}", "tutor", None, None, None, None, {qtd_pets}, {desc_pets})'

    content = re.sub(pattern, replacer, content)

    # Pattern com argumentos nomeados (multilinhas)
    # Procurar Tutor( com argumentos em múltiplas linhas
    def fix_multiline_tutor(text):
        lines = text.split('\n')
        result_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Detectar início de Tutor(
            if re.search(r'tutor\s*=\s*Tutor\s*\(', line, re.IGNORECASE) or re.search(r'Tutor\s*\(', line):
                # Verificar se tem "perfil" nos próximos 15 linhas
                has_perfil = False
                for j in range(i, min(i+15, len(lines))):
                    if 'perfil=' in lines[j] or 'perfil =' in lines[j]:
                        has_perfil = True
                        break
                    if ')' in lines[j] and 'Tutor' not in lines[j]:
                        break

                if not has_perfil:
                    # Procurar onde inserir os novos campos
                    # Inserir após telefone e antes de quantidade_pets
                    for j in range(i, min(i+15, len(lines))):
                        if 'telefone=' in lines[j]:
                            # Encontrou telefone, adicionar os novos campos
                            result_lines.append(lines[j])
                            result_lines.append('            perfil="tutor",')
                            result_lines.append('            foto=None,')
                            result_lines.append('            token_redefinicao=None,')
                            result_lines.append('            data_token=None,')
                            result_lines.append('            data_cadastro=None,')
                            i = j + 1
                            break
                    else:
                        result_lines.append(line)
                        i += 1
                else:
                    result_lines.append(line)
                    i += 1
            else:
                result_lines.append(line)
                i += 1

        return '\n'.join(result_lines)

    content = fix_multiline_tutor(content)
    return content


# Ler o arquivo test_tutor_repo.py
with open('tests/test_tutor_repo.py', 'r', encoding='utf-8') as f:
    content = f.read()

original = content
content = fix_tutor_constructors(content)

if content != original:
    with open('tests/test_tutor_repo.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ test_tutor_repo.py atualizado")
else:
    print("- test_tutor_repo.py sem alterações automáticas")
