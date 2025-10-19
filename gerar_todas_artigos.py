#!/usr/bin/env python3
"""
Script master para processar a geração completa de todas as 100 imagens de artigos.
Este script coordena a geração via Claude Code.
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/Volumes/Externo/Ifes/VetConectaNovo")
PROMPTS_FILE = BASE_DIR / "data" / "prompts_artigos.json"
OUTPUT_DIR = BASE_DIR / "static" / "img" / "artigos"
PROGRESS_FILE = BASE_DIR / "data" / "progresso_artigos.json"

# Imagens já geradas manualmente
GENERATED = {
    1: "https://im.runware.ai/image/ws/2/ii/e1f831f6-a402-4c37-8aa7-ae84c9a7d316.jpg",
    2: "https://im.runware.ai/image/ws/2/ii/50051a28-7843-48d5-9967-775bdb624689.jpg",
    3: "https://im.runware.ai/image/ws/2/ii/d9b6b5e6-1f87-4218-8d6e-275eadd8ec0b.jpg",
    4: "https://im.runware.ai/image/ws/2/ii/8dbf26cd-df47-4381-894a-6c67495e3a21.jpg",
    5: "https://im.runware.ai/image/ws/2/ii/1f78d212-9af2-468c-a9d4-e449c3df4a6c.jpg",
    6: "https://im.runware.ai/image/ws/2/ii/07a58494-ccd2-4202-85d9-23172873080b.jpg",
    7: "https://im.runware.ai/image/ws/2/ii/bb75a7ed-6518-4e16-a116-113017a9c816.jpg",
    8: "https://im.runware.ai/image/ws/2/ii/0e5ca032-8aef-4f12-ae69-ba622e68a562.jpg",
    9: "https://im.runware.ai/image/ws/2/ii/668338c0-4487-4e98-b899-547401c9f4a5.jpg",
    10: "https://im.runware.ai/image/ws/2/ii/246216a6-6536-4453-b889-bdcca4c9a8bc.jpg",
}

def load_prompts():
    """Carrega todos os prompts."""
    with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_progress():
    """Carrega o progresso salvo."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"generated": {}, "downloaded": []}

def save_progress(progress):
    """Salva o progresso."""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def main():
    """Função principal."""
    prompts = load_prompts()
    progress = load_progress()

    # Adicionar as já geradas ao progresso
    for img_id, url in GENERATED.items():
        progress["generated"][str(img_id)] = url

    save_progress(progress)

    print(f"\n{'='*70}")
    print("STATUS DA GERAÇÃO DE IMAGENS DE ARTIGOS")
    print(f"{'='*70}")
    print(f"Total de artigos: {len(prompts)}")
    print(f"Imagens já geradas: {len(progress['generated'])}")
    print(f"Imagens já baixadas: {len(progress['downloaded'])}")
    print(f"Restantes: {len(prompts) - len(progress['generated'])}")
    print(f"{'='*70}\n")

    # Listar as próximas que precisam ser geradas
    print("PRÓXIMAS 10 IMAGENS A GERAR:\n")
    count = 0
    for artigo in prompts:
        if str(artigo['id']) not in progress['generated']:
            count += 1
            print(f"  {artigo['id']:3d}. {artigo['titulo']}")
            if count >= 10:
                break

    remaining = len(prompts) - len(progress['generated'])
    if remaining > 10:
        print(f"\n  ... e mais {remaining - 10} artigos\n")

    print(f"\nCusto estimado para restantes: ${remaining * 0.009:.2f} USD\n")

    # Criar arquivo com lista de IDs e prompts para geração em lote
    to_generate = []
    for artigo in prompts:
        if str(artigo['id']) not in progress['generated']:
            to_generate.append({
                "id": artigo['id'],
                "filename": artigo['filename'],
                "prompt": artigo['prompt'],
                "titulo": artigo['titulo']
            })

    batch_file = BASE_DIR / "data" / "batch_artigos_pendentes.json"
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(to_generate, f, indent=2, ensure_ascii=False)

    print(f"✓ Lista de pendentes salva em: {batch_file}")
    print(f"  Total de imagens a gerar: {len(to_generate)}\n")

if __name__ == "__main__":
    main()
