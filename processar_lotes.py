#!/usr/bin/env python3
"""
Script para organizar prompts em lotes para processamento
"""

import json
from pathlib import Path


def main():
    # Carregar prompts
    prompts_file = Path('data/prompts_feeds_pendentes.json')
    with open(prompts_file, 'r', encoding='utf-8') as f:
        all_prompts = json.load(f)

    # Feeds já processados (181-190)
    processed_ids = set(range(181, 191))

    # Filtrar feeds não processados
    remaining_prompts = [p for p in all_prompts if p['id'] not in processed_ids]

    print(f"Total de imagens restantes: {len(remaining_prompts)}")
    print(f"Primeiro ID: {remaining_prompts[0]['id']}")
    print(f"Último ID: {remaining_prompts[-1]['id']}")
    print()

    # Organizar em lotes de 10
    batch_size = 10
    batches = []

    for i in range(0, len(remaining_prompts), batch_size):
        batch = remaining_prompts[i:i+batch_size]
        batch_num = (i // batch_size) + 2  # +2 porque o lote 1 já foi processado
        batches.append({
            'batch_num': batch_num,
            'start_id': batch[0]['id'],
            'end_id': batch[-1]['id'],
            'count': len(batch),
            'prompts': batch
        })

    # Salvar informações dos lotes
    output_file = Path('data/lotes_pendentes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(batches, f, ensure_ascii=False, indent=2)

    print(f"✓ Arquivo de lotes gerado: {output_file}")
    print(f"✓ Total de lotes: {len(batches)}")
    print()

    # Exibir resumo
    print("RESUMO DOS LOTES:")
    print("=" * 60)
    for batch in batches:
        print(f"Lote {batch['batch_num']:2d}: IDs {batch['start_id']}-{batch['end_id']} ({batch['count']} imagens)")

    print()
    print("Para processar cada lote, use os dados em data/lotes_pendentes.json")


if __name__ == "__main__":
    main()
