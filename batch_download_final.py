#!/usr/bin/env python3
"""
Script final para baixar as últimas 20 imagens (81-100)
"""
import json
import requests
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("/Volumes/Externo/Ifes/VetConectaNovo/static/img/artigos")
LOG_FILE = Path("/Volumes/Externo/Ifes/VetConectaNovo/data/log_geracao_artigos.json")
PROMPTS_FILE = Path("/Volumes/Externo/Ifes/VetConectaNovo/data/prompts_artigos.json")

# Batch final: IDs 81-100
batch = [
    # 81-90
    (81, "https://im.runware.ai/image/ws/2/ii/4fba104e-35b8-474c-b8e2-e1ce286f8f4f.jpg"),
    (82, "https://im.runware.ai/image/ws/2/ii/952eaf3d-bf7f-4d49-b05e-29c521e8f7d2.jpg"),
    (83, "https://im.runware.ai/image/ws/2/ii/38ff4fae-1ff3-41ef-8d46-b1d3948d8b0a.jpg"),
    (84, "https://im.runware.ai/image/ws/2/ii/3ca1b602-2b0a-4893-812d-c4ba720ce96d.jpg"),
    (85, "https://im.runware.ai/image/ws/2/ii/ea412387-3cb3-47ed-90af-4ee53449b523.jpg"),
    (86, "https://im.runware.ai/image/ws/2/ii/a1d44c10-37e6-457a-be26-cb9aa3f5b747.jpg"),
    (87, "https://im.runware.ai/image/ws/2/ii/5c873b7e-f53d-493f-929c-7f41ff96d991.jpg"),
    (88, "https://im.runware.ai/image/ws/2/ii/8002951c-4ae4-487a-a2ba-b305e28f4dad.jpg"),
    (89, "https://im.runware.ai/image/ws/2/ii/341f5394-ab8c-4e7f-a4d8-78cf8e9cb531.jpg"),
    (90, "https://im.runware.ai/image/ws/2/ii/0174f082-9db0-4fb5-ae7c-7ca5204e967a.jpg"),
    # 91-100
    (91, "https://im.runware.ai/image/ws/2/ii/bb13d54c-3e22-44e2-bbb9-ecf68c96f515.jpg"),
    (92, "https://im.runware.ai/image/ws/2/ii/e9ed4a5c-58a4-4c14-9811-b89bb02307ac.jpg"),
    (93, "https://im.runware.ai/image/ws/2/ii/50465caf-72bf-4666-b609-63a06c1d7b96.jpg"),
    (94, "https://im.runware.ai/image/ws/2/ii/c9f71193-cb0a-49a9-ac9f-f823b76952e8.jpg"),
    (95, "https://im.runware.ai/image/ws/2/ii/1dd1da85-a6e0-4b08-919b-ce199006cb87.jpg"),
    (96, "https://im.runware.ai/image/ws/2/ii/dafd7604-bf6d-4186-95f1-5fa3a41863ee.jpg"),
    (97, "https://im.runware.ai/image/ws/2/ii/751b72fe-d9c1-4153-84bf-9207d3501b6b.jpg"),
    (98, "https://im.runware.ai/image/ws/2/ii/bce0a88a-22b6-4a14-b84e-9857e94a5ba3.jpg"),
    (99, "https://im.runware.ai/image/ws/2/ii/310779a6-ab8e-4860-846e-c020e31144c0.jpg"),
    (100, "https://im.runware.ai/image/ws/2/ii/68fb4b10-7879-45b7-a46f-4f346c953b17.jpg"),
]

print("=" * 70)
print("DOWNLOAD FINAL - IMAGENS 81-100")
print("=" * 70)

with open(PROMPTS_FILE, 'r') as f:
    artigos = json.load(f)

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
    print(f"\n[{artigo_id}/100] {artigo['titulo']}")

    if filepath.exists():
        print(f"  ⏭️  Já existe: {artigo['filename']}")
        success += 1
        continue

    print(f"  ⬇️  Baixando...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        file_size = filepath.stat().st_size / 1024  # KB
        print(f"  ✅ Salvo: {artigo['filename']} ({file_size:.1f} KB)")

        log_entries.append({
            "id": artigo_id,
            "titulo": artigo['titulo'],
            "filename": artigo['filename'],
            "url": url,
            "status": "success",
            "file_size_kb": round(file_size, 1),
            "generated_at": datetime.now().isoformat()
        })

        success += 1

    except Exception as e:
        print(f"  ❌ ERRO: {e}")

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

print("\n" + "=" * 70)
print("RESUMO FINAL")
print("=" * 70)

existing = sorted(OUTPUT_DIR.glob('*.jpg'))
print(f"\n✅ Imagens baixadas com sucesso: {success}/{len(batch)}")
print(f"❌ Falhas: {failed}/{len(batch)}")
print(f"\n📊 TOTAL DE IMAGENS: {len(existing)}/100")

if len(existing) == 100:
    print("\n🎉 TODAS AS 100 IMAGENS FORAM GERADAS COM SUCESSO!")

    # Calcular tamanho total
    total_size = sum(f.stat().st_size for f in existing) / (1024 * 1024)  # MB
    print(f"📦 Tamanho total: {total_size:.2f} MB")
    print(f"📈 Média por imagem: {total_size/100:.2f} MB")
else:
    pending = 100 - len(existing)
    print(f"\n⏳ Ainda faltam: {pending} imagens")

print(f"\n📝 Log completo salvo em:")
print(f"   {LOG_FILE}")

print(f"\n📁 Diretório de imagens:")
print(f"   {OUTPUT_DIR}")

print("\n" + "=" * 70)
