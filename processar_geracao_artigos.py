#!/usr/bin/env python3
"""
Script para processar o download das imagens geradas.
"""

import json
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/Volumes/Externo/Ifes/VetConectaNovo")
OUTPUT_DIR = BASE_DIR / "static" / "img" / "artigos"
LOG_FILE = BASE_DIR / "data" / "log_download_artigos.json"

# Garantir que diretório existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# URLs das primeiras 5 imagens geradas
images_generated = [
    {
        "id": 1,
        "filename": "00000001.jpg",
        "url": "https://im.runware.ai/image/ws/2/ii/e1f831f6-a402-4c37-8aa7-ae84c9a7d316.jpg"
    },
    {
        "id": 2,
        "filename": "00000002.jpg",
        "url": "https://im.runware.ai/image/ws/2/ii/50051a28-7843-48d5-9967-775bdb624689.jpg"
    },
    {
        "id": 3,
        "filename": "00000003.jpg",
        "url": "https://im.runware.ai/image/ws/2/ii/d9b6b5e6-1f87-4218-8d6e-275eadd8ec0b.jpg"
    },
    {
        "id": 4,
        "filename": "00000004.jpg",
        "url": "https://im.runware.ai/image/ws/2/ii/8dbf26cd-df47-4381-894a-6c67495e3a21.jpg"
    },
    {
        "id": 5,
        "filename": "00000005.jpg",
        "url": "https://im.runware.ai/image/ws/2/ii/1f78d212-9af2-468c-a9d4-e449c3df4a6c.jpg"
    }
]

log = {
    "timestamp": datetime.now().isoformat(),
    "downloaded": [],
    "failed": []
}

print(f"\n{'='*70}")
print("BAIXANDO IMAGENS GERADAS")
print(f"{'='*70}\n")

for img in images_generated:
    filepath = OUTPUT_DIR / img["filename"]
    print(f"Baixando imagem {img['id']}: {img['filename']}... ", end="", flush=True)

    try:
        response = requests.get(img["url"], timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ OK ({len(response.content)} bytes)")
        log["downloaded"].append({
            "id": img["id"],
            "filename": img["filename"],
            "size": len(response.content)
        })

    except Exception as e:
        print(f"✗ ERRO: {e}")
        log["failed"].append({
            "id": img["id"],
            "filename": img["filename"],
            "error": str(e)
        })

# Salvar log
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2, ensure_ascii=False)

print(f"\n{'='*70}")
print("RESUMO")
print(f"{'='*70}")
print(f"Baixadas: {len(log['downloaded'])}")
print(f"Falhas: {len(log['failed'])}")
print(f"Log salvo em: {LOG_FILE}")
print(f"{'='*70}\n")
