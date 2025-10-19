#!/usr/bin/env python3
"""
Script simplificado para processar imagens de artigos.
Gera uma lista de comandos para o Claude Code executar.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Ler prompts
prompts_path = BASE_DIR / "data" / "prompts_artigos.json"
with open(prompts_path, 'r', encoding='utf-8') as f:
    prompts_data = json.load(f)

output_dir = BASE_DIR / "static" / "img" / "artigos"

print("# Comandos para gerar imagens dos artigos")
print("# Execute cada bloco no Claude Code\n")

# Dividir em lotes de 10
batch_size = 10
for i in range(0, len(prompts_data), batch_size):
    batch = prompts_data[i:i+batch_size]
    batch_num = (i // batch_size) + 1

    print(f"\n## LOTE {batch_num} (Artigos {batch[0]['id']} a {batch[-1]['id']})")
    print(f"## Total: {len(batch)} imagens\n")

    for item in batch:
        filename = output_dir / item['filename']

        print(f"# ID {item['id']}: {item['titulo']}")
        print(f"# Arquivo: {item['filename']}")
        print(f"Prompt: {item['prompt']}")
        print(f"Download para: {filename}")
        print()

    print(f"## Fim do lote {batch_num}")
    print("-" * 80)
