#!/usr/bin/env python3
"""
Script para gerar imagens para todos os artigos veterinários usando Runware AI.
"""

import json
import os
import sys
import requests
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent
PROMPTS_FILE = BASE_DIR / "data" / "prompts_artigos.json"
OUTPUT_DIR = BASE_DIR / "static" / "img" / "artigos"
LOG_FILE = BASE_DIR / "data" / "log_geracao_artigos.json"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "data").mkdir(exist_ok=True)


def load_prompts():
    """Carrega o arquivo de prompts."""
    with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def download_image(url: str, filepath: Path) -> bool:
    """Baixa uma imagem da URL e salva no filepath."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        return True
    except Exception as e:
        print(f"  ❌ Erro ao baixar: {e}")
        return False


def generate_images():
    """Gera todas as imagens dos artigos."""

    # Load prompts
    print("📖 Carregando prompts...")
    artigos = load_prompts()
    total = len(artigos)
    print(f"✅ {total} artigos encontrados\n")

    # Statistics
    generated = 0
    skipped = 0
    failed = 0

    # Load existing log if it exists
    log_entries = []
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            log_entries = json.load(f)

    # Process each article
    for idx, artigo in enumerate(artigos, 1):
        artigo_id = artigo['id']
        titulo = artigo['titulo']
        prompt = artigo['prompt']
        filename = artigo['filename']
        filepath = OUTPUT_DIR / filename

        print(f"[{idx}/{total}] {titulo}")

        # Skip if already exists
        if filepath.exists():
            print(f"  ⏭️  Já existe: {filename}")
            skipped += 1
            continue

        # Generate image using MCP tool (we'll need to call this manually)
        # For now, we'll prepare the data structure and let the user run via Claude
        print(f"  🎨 Gerando imagem com Runware AI...")
        print(f"     Prompt: {prompt[:80]}...")

        # Log entry template
        log_entry = {
            "id": artigo_id,
            "titulo": titulo,
            "filename": filename,
            "prompt": prompt,
            "status": "pending",
            "generated_at": datetime.now().isoformat(),
            "url": None,
            "error": None
        }

        log_entries.append(log_entry)

    # Save pending log
    print(f"\n📊 Resumo:")
    print(f"   ✅ Já existem: {skipped}")
    print(f"   ⏳ Pendentes: {total - skipped}")

    # Save log
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_entries, f, indent=2, ensure_ascii=False)

    print(f"\n📝 Log salvo em: {LOG_FILE}")
    print(f"\n⚠️  ATENÇÃO: Este script preparou os dados.")
    print(f"   Execute o processamento via Claude Code para gerar as imagens.")

    return {
        "total": total,
        "skipped": skipped,
        "pending": total - skipped
    }


if __name__ == "__main__":
    try:
        stats = generate_images()
        print(f"\n✅ Processo concluído!")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)
