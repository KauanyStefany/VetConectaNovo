#!/usr/bin/env python3
"""
Script master para coordenar a geração de todas as imagens.
Este script organiza o trabalho e mostra o progresso.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def main():
    # Ler prompts
    prompts_file = BASE_DIR / "data" / "prompts_artigos.json"
    with open(prompts_file, 'r') as f:
        all_prompts = json.load(f)

    output_dir = BASE_DIR / "static" / "img" / "artigos"

    print(f"═" * 70)
    print(f"  GERAÇÃO DE IMAGENS DE ARTIGOS")
    print(f"═" * 70)
    print(f"\nTotal de artigos: {len(all_prompts)}")
    print(f"Custo estimado: ${len(all_prompts) * 0.009:.2f}")
    print(f"\nEste processo irá:")
    print(f"  1. Gerar {len(all_prompts)} imagens via Runware AI")
    print(f"  2. Baixar e salvar em {output_dir}")
    print(f"  3. Criar log de processamento")

    print(f"\n{'─' * 70}")
    print(f"IMPORTANTE: As imagens serão geradas usando a ferramenta")
    print(f"mcp__runware__generate_image disponível no Claude Code")
    print(f"{'─' * 70}")

    # Exportar informações para processamento
    for idx, prompt_data in enumerate(all_prompts, 1):
        filename = output_dir / prompt_data['filename']

        if filename.exists():
            status = "✓ EXISTE"
        else:
            status = "⏳ PENDENTE"

        if idx <= 10 or idx > len(all_prompts) - 3:
            print(f"\n[{idx:3d}/{len(all_prompts)}] {status}")
            print(f"  Título: {prompt_data['titulo'][:65]}")
            print(f"  Arquivo: {prompt_data['filename']}")
            print(f"  Prompt: {prompt_data['prompt'][:70]}...")
        elif idx == 11:
            print(f"\n  ... ({len(all_prompts) - 13} artigos) ...")

    print(f"\n{'═' * 70}")
    print(f"Pronto para processar! Use o Claude Code para gerar as imagens.")
    print(f"{'═' * 70}\n")

if __name__ == "__main__":
    main()
