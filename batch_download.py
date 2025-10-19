#!/usr/bin/env python3
"""
Script para baixar imagens em lote
"""

import json
import requests
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("/Volumes/Externo/Ifes/VetConectaNovo/static/img/artigos")
LOG_FILE = Path("/Volumes/Externo/Ifes/VetConectaNovo/data/log_geracao_artigos.json")
PROMPTS_FILE = Path("/Volumes/Externo/Ifes/VetConectaNovo/data/prompts_artigos.json")

# Batch atual: IDs 57-66
batch = [
    (57, "https://im.runware.ai/image/ws/2/ii/5c7b3a35-b16a-4918-8cac-428fb33aeda9.jpg"),
    (58, "https://im.runware.ai/image/ws/2/ii/6eb40e8a-907a-4335-82d8-cc1f53fbb16d.jpg"),
    (59, "https://im.runware.ai/image/ws/2/ii/e70dade2-3065-4624-907f-8231e1f32f6b.jpg"),
    (60, "https://im.runware.ai/image/ws/2/ii/59b5e594-ad42-4272-9b73-5bd153c2ce42.jpg"),
    (61, "https://im.runware.ai/image/ws/2/ii/5af97f87-7cf9-4502-9500-e0a6b1fd8d70.jpg"),
    (62, "https://im.runware.ai/image/ws/2/ii/4a049900-077d-4a3f-815b-f903ff632891.jpg"),
    (63, "https://im.runware.ai/image/ws/2/ii/ab950bce-61a6-43b0-a18c-7d188e87f374.jpg"),
    (64, "https://im.runware.ai/image/ws/2/ii/09bc7eca-8b0c-4a91-b3d3-5d6f938afdaf.jpg"),
    (65, "https://im.runware.ai/image/ws/2/ii/b63766b5-974a-4401-9a24-fd1e7c78877b.jpg"),
    (66, "https://im.runware.ai/image/ws/2/ii/cf285015-6d28-4643-ac52-e078f42370c3.jpg"),
]

# Load prompts
with open(PROMPTS_FILE, 'r') as f:
    artigos = json.load(f)

# Load log
if LOG_FILE.exists():
    with open(LOG_FILE, 'r') as f:
        log_entries = json.load(f)
else:
    log_entries = []

success = 0
failed = 0

for artigo_id, url in batch:
    artigo = next(a for a in artigos if a['id'] == artigo_id)
    filepath = OUTPUT_DIR / artigo['filename']

    print(f"[{artigo_id}/100] {artigo['titulo'][:50]}")

    if filepath.exists():
        print(f"  ⏭️  Já existe")
        success += 1
        continue

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"  ✅ Salvo")

        log_entries.append({
            "id": artigo_id,
            "titulo": artigo['titulo'],
            "filename": artigo['filename'],
            "url": url,
            "status": "success",
            "generated_at": datetime.now().isoformat()
        })

        success += 1

    except Exception as e:
        print(f"  ❌ Erro: {e}")

        log_entries.append({
            "id": artigo_id,
            "titulo": artigo['titulo'],
            "filename": artigo['filename'],
            "url": url,
            "status": "failed",
            "error": str(e),
            "generated_at": datetime.now().isoformat()
        })

        failed += 1

# Save log
with open(LOG_FILE, 'w') as f:
    json.dump(log_entries, f, indent=2, ensure_ascii=False)

print(f"\n✅ Sucesso: {success}/{len(batch)}")
print(f"❌ Falhas: {failed}/{len(batch)}")
print(f"📝 Log: {LOG_FILE}")

# Status geral
existing = len(list(OUTPUT_DIR.glob('*.jpg')))
print(f"\n📊 Status Geral: {existing}/100 imagens completas")
print(f"⏳ Pendentes: {100 - existing}")
