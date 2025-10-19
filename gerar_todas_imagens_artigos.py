#!/usr/bin/env python3
"""
Script para gerar TODAS as imagens de artigos automaticamente.
Este script lista os comandos necessários para o Claude Code processar.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Ler prompts
prompts_path = BASE_DIR / "data" / "prompts_artigos.json"
with open(prompts_path, 'r', encoding='utf-8') as f:
    all_prompts = json.load(f)

output_dir = BASE_DIR / "static" / "img" / "artigos"

# Criar estrutura de dados para processamento
to_process = []

for item in all_prompts:
    filename_path = output_dir / item['filename']

    # Verificar se já existe
    if not filename_path.exists():
        to_process.append({
            'id': item['id'],
            'filename': str(filename_path),
            'prompt': item['prompt'],
            'titulo': item['titulo']
        })

print(f"Total de imagens a gerar: {len(to_process)}")
print(f"Já existentes: {len(all_prompts) - len(to_process)}")

# Salvar lista de processamento
process_file = BASE_DIR / "data" / "processar_imagens_pendentes.json"
with open(process_file, 'w', encoding='utf-8') as f:
    json.dump(to_process, f, indent=2, ensure_ascii=False)

print(f"\nLista salva em: {process_file}")
print(f"\nPrimeiras 5 imagens a processar:")
for item in to_process[:5]:
    print(f"  {item['id']:3d}. {item['titulo'][:60]}")
