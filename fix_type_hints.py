#!/usr/bin/env python3
"""Script para adicionar asserções de tipo nos testes."""

import re
from pathlib import Path
from typing import List, Tuple


def add_assertions_to_file(file_path: Path) -> int:
    """Adiciona asserções após chamadas que retornam Optional[int]."""
    content = file_path.read_text(encoding='utf-8')
    lines = content.split('\n')
    new_lines: List[str] = []
    changes = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        # Padrão: id_algo = inserir(...) ou id_algo = repo.inserir(...)
        match = re.match(r'^(\s+)(id_\w+)\s*=\s*\w+\.?inserir\(', line)
        if match:
            indent = match.group(1)
            var_name = match.group(2)
            # Verifica se já não tem assert na próxima linha
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if f'assert {var_name} is not None' not in next_line:
                    new_lines.append(f'{indent}assert {var_name} is not None')
                    changes += 1

        # Padrão: objeto_db = obter_por_id(...) ou objeto = repo.obter_por_id(...)
        match = re.match(r'^(\s+)(\w+)\s*=\s*\w+\.?obter_\w+\(', line)
        if match and i + 1 < len(lines):
            indent = match.group(1)
            var_name = match.group(2)
            next_line = lines[i + 1]
            # Só adiciona assert se a próxima linha não for um assert ou comentário
            if (not next_line.strip().startswith('assert') and
                not next_line.strip().startswith('#') and
                next_line.strip() and
                'assert' in next_line and var_name in next_line):
                # Já tem um assert na próxima linha, pula
                pass
            elif (not next_line.strip().startswith('assert') and
                  not next_line.strip().startswith('#') and
                  next_line.strip()):
                # Verifica se a variável é usada na linha seguinte (indicando que não deveria ser None)
                if var_name in next_line and '=' not in next_line.split(var_name)[0]:
                    new_lines.append(f'{indent}assert {var_name} is not None')
                    changes += 1

        i += 1

    if changes > 0:
        file_path.write_text('\n'.join(new_lines), encoding='utf-8')

    return changes


def main():
    """Processa todos os arquivos de teste."""
    tests_dir = Path('tests')
    total_changes = 0

    for file_path in tests_dir.glob('test_*.py'):
        changes = add_assertions_to_file(file_path)
        if changes > 0:
            print(f'{file_path.name}: {changes} asserções adicionadas')
            total_changes += changes

    print(f'\nTotal: {total_changes} asserções adicionadas')


if __name__ == '__main__':
    main()
