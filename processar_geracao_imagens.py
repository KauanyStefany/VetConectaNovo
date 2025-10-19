#!/usr/bin/env python3
"""
Script auxiliar para baixar imagens já geradas via MCP
"""

import requests
import json
from pathlib import Path
from datetime import datetime

# Imagens já geradas (IDs 49-51)
generated_images = [
    {
        "id": 49,
        "filename": "00000049.jpg",
        "url": "https://im.runware.ai/image/ws/2/ii/41f0308c-020c-4ab9-8d0f-b5ae65f2c0c0.jpg",
        "titulo": "Eliminação inapropriada em gatos"
    },
    {
        "id": 50,
        "filename": "00000050.jpg",
        "url": "https://im.runware.ai/image/ws/2/ii/501375df-ab5a-488e-b73d-361ae084cf33.jpg",
        "titulo": "Socialização de filhotes: período crítico"
    },
    {
        "id": 51,
        "filename": "00000051.jpg",
        "url": "https://im.runware.ai/image/ws/2/ii/b935e269-1424-4172-8bdf-38555a7495bd.jpg",
        "titulo": "Inseminação artificial em bovinos"
    }
]

OUTPUT_DIR = Path("/Volumes/Externo/Ifes/VetConectaNovo/static/img/artigos")
LOG_FILE = Path("/Volumes/Externo/Ifes/VetConectaNovo/data/log_geracao_artigos.json")

# Load existing log
if LOG_FILE.exists():
    with open(LOG_FILE, 'r') as f:
        log_entries = json.load(f)
else:
    log_entries = []

# Download and log
for img in generated_images:
    filepath = OUTPUT_DIR / img['filename']

    if filepath.exists():
        print(f"✅ [{img['id']}] Já existe: {img['filename']}")
        continue

    print(f"⬇️  [{img['id']}] Baixando: {img['titulo']}")

    try:
        response = requests.get(img['url'], timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"    ✅ Salvo: {filepath}")

        # Add to log
        log_entries.append({
            "id": img['id'],
            "titulo": img['titulo'],
            "filename": img['filename'],
            "url": img['url'],
            "status": "success",
            "generated_at": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"    ❌ Erro: {e}")
        log_entries.append({
            "id": img['id'],
            "titulo": img['titulo'],
            "filename": img['filename'],
            "url": img['url'],
            "status": "failed",
            "error": str(e),
            "generated_at": datetime.now().isoformat()
        })

# Save log
with open(LOG_FILE, 'w') as f:
    json.dump(log_entries, f, indent=2, ensure_ascii=False)

print(f"\n📝 Log atualizado: {LOG_FILE}")
