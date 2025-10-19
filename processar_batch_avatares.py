#!/usr/bin/env python3
"""
Script auxiliar para processar avatares em lotes
Gera comandos de download em batch
"""

import json
from pathlib import Path


def gerar_script_download(inicio, fim, urls_dict):
    """Gera script de download para um lote"""
    commands = []
    for i in range(inicio, fim + 1):
        if i in urls_dict:
            commands.append(f'curl -s -o "static/img/usuarios/{i:08d}.jpg" "{urls_dict[i]}"')

    script = " && ".join(commands)
    script += f' && echo "✓ IDs {inicio}-{fim} baixados!"'
    return script


def main():
    # Lê prompts
    with open('data/prompts_usuarios.json', 'r', encoding='utf-8') as f:
        users = json.load(f)

    # Exibe próximo lote
    print("PRÓXIMO LOTE (61-80):")
    print("=" * 80)
    for user in users[60:80]:
        print(f"ID {user['id_usuario']}: {user['prompt'][:80]}...")
        print()


if __name__ == "__main__":
    main()
