#!/usr/bin/env python3
import json
import requests
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("/Volumes/Externo/Ifes/VetConectaNovo/static/img/artigos")
LOG_FILE = Path("/Volumes/Externo/Ifes/VetConectaNovo/data/log_geracao_artigos.json")
PROMPTS_FILE = Path("/Volumes/Externo/Ifes/VetConectaNovo/data/prompts_artigos.json")

# Batch: IDs 67-80
batch = [
    (67, "https://im.runware.ai/image/ws/2/ii/ba62ee15-b5e8-4e66-a756-af29c927ca1e.jpg"),
    (68, "https://im.runware.ai/image/ws/2/ii/01b0dffd-2502-4188-8378-8596fb397770.jpg"),
    (69, "https://im.runware.ai/image/ws/2/ii/25fd2576-a637-4ec6-9e2c-766e1186478a.jpg"),
    (70, "https://im.runware.ai/image/ws/2/ii/c1c0fafc-1138-4827-a673-9105e185b5f2.jpg"),
    (71, "https://im.runware.ai/image/ws/2/ii/475e087e-15f4-4bce-9b19-9b065427f83a.jpg"),
    (72, "https://im.runware.ai/image/ws/2/ii/073d4c32-b37f-409a-9b7e-d53739a7df1b.jpg"),
    (73, "https://im.runware.ai/image/ws/2/ii/8132b80a-7904-4a3c-94d4-88e96b151802.jpg"),
    (74, "https://im.runware.ai/image/ws/2/ii/c1a55a12-b92b-44df-8db1-d0cbf78aef69.jpg"),
    (75, "https://im.runware.ai/image/ws/2/ii/464ce8ba-8e19-4510-930d-25531058d428.jpg"),
    (76, "https://im.runware.ai/image/ws/2/ii/300d6244-34d1-4d55-a994-1a28dd92c3a6.jpg"),
    (77, "https://im.runware.ai/image/ws/2/ii/9cf5ec05-620d-4d2b-b151-8ea5b08dc5dd.jpg"),
    (78, "https://im.runware.ai/image/ws/2/ii/5d6b56ff-98c0-46c8-b721-a4fb59f38450.jpg"),
    (79, "https://im.runware.ai/image/ws/2/ii/0bc26238-d34b-468b-9ad3-72134d193f4b.jpg"),
    (80, "https://im.runware.ai/image/ws/2/ii/e148c3e2-c01f-440d-8141-65c1dd8cbd71.jpg"),
]

with open(PROMPTS_FILE, 'r') as f:
    artigos = json.load(f)

if LOG_FILE.exists():
    with open(LOG_FILE, 'r') as f:
        log_entries = json.load(f)
else:
    log_entries = []

success = 0
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

with open(LOG_FILE, 'w') as f:
    json.dump(log_entries, f, indent=2, ensure_ascii=False)

existing = len(list(OUTPUT_DIR.glob('*.jpg')))
print(f"\n✅ Sucesso: {success}/{len(batch)}")
print(f"📊 Total: {existing}/100 imagens")
print(f"⏳ Pendentes: {100 - existing}")
