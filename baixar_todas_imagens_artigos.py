#!/usr/bin/env python3
"""
Script para baixar todas as 100 imagens de artigos geradas pela API Runware.
"""

import json
import requests
from pathlib import Path
from datetime import datetime
import time

BASE_DIR = Path("/Volumes/Externo/Ifes/VetConectaNovo")
OUTPUT_DIR = BASE_DIR / "static" / "img" / "artigos"
LOG_FILE = BASE_DIR / "data" / "log_download_completo_artigos.json"

# Garantir que diretório existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Mapeamento completo de todas as 100 imagens geradas
IMAGES_MAP = {
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
    11: "https://im.runware.ai/image/ws/2/ii/090490b6-e5ae-4190-9aa3-548054fc01c9.jpg",
    12: "https://im.runware.ai/image/ws/2/ii/859eb2a8-8bda-4481-85ed-6089ec557484.jpg",
    13: "https://im.runware.ai/image/ws/2/ii/cd38a819-01c6-4049-aa38-63638fb78ee7.jpg",
    14: "https://im.runware.ai/image/ws/2/ii/4cd522af-ab46-4b8a-bb78-486c1fb766cb.jpg",
    15: "https://im.runware.ai/image/ws/2/ii/ee32885e-8f90-45d2-a2f1-510b6cdc6b43.jpg",
    16: "https://im.runware.ai/image/ws/2/ii/43c2cfe6-353a-4542-b3f9-acd9a44a0890.jpg",
    17: "https://im.runware.ai/image/ws/2/ii/f252b7fd-501d-43e6-b6f8-22c59a1d6b94.jpg",
    18: "https://im.runware.ai/image/ws/2/ii/581167fb-34c5-4260-86c1-5d3167c23f62.jpg",
    19: "https://im.runware.ai/image/ws/2/ii/03112b92-a1ff-4f26-bb4c-b52d2057c100.jpg",
    20: "https://im.runware.ai/image/ws/2/ii/1527b66f-d5e2-4429-b84a-614052f02acf.jpg",
    21: "https://im.runware.ai/image/ws/2/ii/76c20902-aff6-4502-95d3-d1511e58ab07.jpg",
    22: "https://im.runware.ai/image/ws/2/ii/cd9e1009-464b-4b00-b6ca-7388b956fe47.jpg",
    23: "https://im.runware.ai/image/ws/2/ii/0436b030-ca64-45d4-b688-026642717ea5.jpg",
    24: "https://im.runware.ai/image/ws/2/ii/2b256709-ead1-47a2-aefa-bfee9486bb56.jpg",
    25: "https://im.runware.ai/image/ws/2/ii/5fa71b4d-a309-4d4e-9c3c-e6d160b490ac.jpg",
    26: "https://im.runware.ai/image/ws/2/ii/2573764e-6b78-49b9-96d6-16fc6f7082b6.jpg",
    27: "https://im.runware.ai/image/ws/2/ii/6bfe1a13-ec71-4bfe-8fa3-b2109e005a2a.jpg",
    28: "https://im.runware.ai/image/ws/2/ii/3d99fa5e-37c2-4ca2-ade1-bccafb36554f.jpg",
    29: "https://im.runware.ai/image/ws/2/ii/985a5554-cf46-40b1-b6ed-4fd367c9f1a3.jpg",
    30: "https://im.runware.ai/image/ws/2/ii/39343a33-c2d0-49ae-abf3-bafb59bd99ca.jpg",
    31: "https://im.runware.ai/image/ws/2/ii/cb03e3bb-069f-4ba1-b73e-c7fe22debe4f.jpg",
    32: "https://im.runware.ai/image/ws/2/ii/dc9e40d7-464e-46f8-96d2-c0a67019124c.jpg",
    33: "https://im.runware.ai/image/ws/2/ii/9d9fe134-ef9b-44db-b550-0a250b8e1443.jpg",
    34: "https://im.runware.ai/image/ws/2/ii/7ca7fc6e-4610-4fd3-92b2-25a16bf7e5ed.jpg",
    35: "https://im.runware.ai/image/ws/2/ii/618ef308-5a14-4f3d-aaf1-1e599c96baed.jpg",
    36: "https://im.runware.ai/image/ws/2/ii/6999b056-df01-4f21-a710-9752bc0437ea.jpg",
    37: "https://im.runware.ai/image/ws/2/ii/e4a5e0be-61c6-43f7-8cdb-c3b28b99401c.jpg",
    38: "https://im.runware.ai/image/ws/2/ii/3a63e366-aee0-41bf-bdbe-c2e99047a5ff.jpg",
    39: "https://im.runware.ai/image/ws/2/ii/91cebe96-6a2f-4a89-83db-5c7c312d38d8.jpg",
    40: "https://im.runware.ai/image/ws/2/ii/a9b29f6e-45b7-46fb-b321-a90d19c49536.jpg",
    41: "https://im.runware.ai/image/ws/2/ii/1366dd57-f6f9-48a4-b54d-ea07bfa6e300.jpg",
    42: "https://im.runware.ai/image/ws/2/ii/a212f623-d90a-4d68-af38-034942a4184f.jpg",
    43: "https://im.runware.ai/image/ws/2/ii/b63c4ecc-a434-4d2d-a950-6374a9aad9d2.jpg",
    44: "https://im.runware.ai/image/ws/2/ii/de0acee3-684e-455a-97ed-ee5f8ba0aedc.jpg",
    45: "https://im.runware.ai/image/ws/2/ii/9703f186-68dd-4e02-bf35-66c66081e1e7.jpg",
    46: "https://im.runware.ai/image/ws/2/ii/bbedb0da-9b9f-48c0-874e-25153d45ede9.jpg",
    47: "https://im.runware.ai/image/ws/2/ii/6bf2a03e-7326-4e3f-928c-d09f55b2b77c.jpg",
    48: "https://im.runware.ai/image/ws/2/ii/bddeb678-e88b-405b-8e96-5904d796e878.jpg",
    49: "https://im.runware.ai/image/ws/2/ii/210f9ef3-0cee-4f93-9456-3368d9ec4146.jpg",
    50: "https://im.runware.ai/image/ws/2/ii/db1566b2-42cc-4d2a-b0fe-40e6f23a0b06.jpg",
    51: "https://im.runware.ai/image/ws/2/ii/928341c1-46cc-4adc-be39-aec8b7628bd3.jpg",
    52: "https://im.runware.ai/image/ws/2/ii/b06080e6-0a1b-4e94-8c15-79caef51553f.jpg",
    53: "https://im.runware.ai/image/ws/2/ii/fcc3db9d-c9a8-4c00-aabf-e6f2735592f1.jpg",
    54: "https://im.runware.ai/image/ws/2/ii/107c21f6-2bee-4265-9279-0e2a13668221.jpg",
    55: "https://im.runware.ai/image/ws/2/ii/a65355f6-bd2c-490d-b09f-9de1c9f61679.jpg",
    56: "https://im.runware.ai/image/ws/2/ii/08f463e4-1bf1-4ebc-8ccf-b4e4670ab374.jpg",
    57: "https://im.runware.ai/image/ws/2/ii/44f1c42c-ecb7-4a8c-9f09-67da171d5950.jpg",
    58: "https://im.runware.ai/image/ws/2/ii/b4460634-93e6-4469-84bd-437ba7e010fc.jpg",
    59: "https://im.runware.ai/image/ws/2/ii/2e3dabbd-8867-4773-ac4f-8417e0854b11.jpg",
    60: "https://im.runware.ai/image/ws/2/ii/a4933739-e088-4266-bafd-46e0c527768a.jpg",
    61: "https://im.runware.ai/image/ws/2/ii/72ca6243-df4e-4fde-9fc0-6010dfea6e42.jpg",
    62: "https://im.runware.ai/image/ws/2/ii/e8b75e13-11f1-416e-a169-5af0a64d9460.jpg",
    63: "https://im.runware.ai/image/ws/2/ii/4b418996-46f0-4c1f-934a-7bb0868756cc.jpg",
    64: "https://im.runware.ai/image/ws/2/ii/6bc3bffc-1efa-42b6-bca8-5defdb18abc3.jpg",
    65: "https://im.runware.ai/image/ws/2/ii/0bd1fcad-a1bb-4040-b91c-e99142bd3939.jpg",
    66: "https://im.runware.ai/image/ws/2/ii/c9e3b5c3-8b59-491e-a5f0-bcf9db7e9fe1.jpg",
    67: "https://im.runware.ai/image/ws/2/ii/c68b1272-52f8-4810-b759-91be3cbae995.jpg",
    68: "https://im.runware.ai/image/ws/2/ii/7f603c10-80b4-4609-8f16-5bd558dd3113.jpg",
    69: "https://im.runware.ai/image/ws/2/ii/b0874607-a047-4500-b1a7-f2742e4992dd.jpg",
    70: "https://im.runware.ai/image/ws/2/ii/e936cbfe-a5a0-4945-8520-59cb6bf9597f.jpg",
    71: "https://im.runware.ai/image/ws/2/ii/10f79fb9-2dc8-466c-a662-1aaa1f01ce08.jpg",
    72: "https://im.runware.ai/image/ws/2/ii/a2047534-6ad3-432e-a0c6-e71a9b9d2227.jpg",
    73: "https://im.runware.ai/image/ws/2/ii/17dbee85-ad91-4d96-b7d4-70d748839454.jpg",
    74: "https://im.runware.ai/image/ws/2/ii/4fb4fe26-5ec4-4e56-a381-abeffb194f75.jpg",
    75: "https://im.runware.ai/image/ws/2/ii/35f88de7-b1e0-4cfb-b980-cc92fc330412.jpg",
    76: "https://im.runware.ai/image/ws/2/ii/b58cb4f8-7497-416c-b31d-d80ff8d8cceb.jpg",
    77: "https://im.runware.ai/image/ws/2/ii/132fd787-d613-43bd-86f3-34cf6313e811.jpg",
    78: "https://im.runware.ai/image/ws/2/ii/1f1a354b-50a9-4e0b-80aa-fb634b8cb61d.jpg",
    79: "https://im.runware.ai/image/ws/2/ii/332d4555-f8e5-4b84-84d4-89605d3f4a85.jpg",
    80: "https://im.runware.ai/image/ws/2/ii/a32f49d9-97d2-47c5-a889-21762d9080e2.jpg",
    81: "https://im.runware.ai/image/ws/2/ii/a5b4a791-3e7c-45a2-8e1e-510887cf6f20.jpg",
    82: "https://im.runware.ai/image/ws/2/ii/a7c1fe07-92c7-415d-93e5-f97d34ce84b4.jpg",
    83: "https://im.runware.ai/image/ws/2/ii/266c5ee9-1e70-4aa3-993d-86edfc342c67.jpg",
    84: "https://im.runware.ai/image/ws/2/ii/1388a6e1-3346-4e97-ac60-9ec0860b6a54.jpg",
    85: "https://im.runware.ai/image/ws/2/ii/27f72f03-737b-42d6-a18b-1f726db23bf7.jpg",
    86: "https://im.runware.ai/image/ws/2/ii/07c98565-9108-49ea-a8fc-66a4602c33c1.jpg",
    87: "https://im.runware.ai/image/ws/2/ii/222aaa8d-0017-413d-8998-805f8411ccbc.jpg",
    88: "https://im.runware.ai/image/ws/2/ii/38d10a01-fb3c-4a82-9873-4b9ff035bd1d.jpg",
    89: "https://im.runware.ai/image/ws/2/ii/dc82f3f9-0681-47f8-a235-24e25bd03382.jpg",
    90: "https://im.runware.ai/image/ws/2/ii/1b4bacfa-62be-428d-8956-2b395b4c1482.jpg",
    91: "https://im.runware.ai/image/ws/2/ii/9de9c98e-a4e5-4c32-8410-f0794381b6a8.jpg",
    92: "https://im.runware.ai/image/ws/2/ii/c9de50e2-2dfc-45eb-9234-c54b877008d2.jpg",
    93: "https://im.runware.ai/image/ws/2/ii/4f154638-e7f2-4c1e-8b82-c6718f9ce524.jpg",
    94: "https://im.runware.ai/image/ws/2/ii/8f3018bc-dae7-4648-82b1-93ed01c82ba2.jpg",
    95: "https://im.runware.ai/image/ws/2/ii/d9c6b1d3-c38d-4284-9120-1634614f8133.jpg",
    96: "https://im.runware.ai/image/ws/2/ii/f2426fa1-0a52-4d5d-ad6d-6dd3f4f2c02b.jpg",
    97: "https://im.runware.ai/image/ws/2/ii/f18e865c-e1e7-4afd-b4f1-aa3c69663633.jpg",
    98: "https://im.runware.ai/image/ws/2/ii/c2080e3f-32d6-4832-ab6a-7c6becd391e0.jpg",
    99: "https://im.runware.ai/image/ws/2/ii/556c101a-bb8a-44d1-91eb-5e4bcd6c51ff.jpg",
    100: "https://im.runware.ai/image/ws/2/ii/eea18a81-9332-4eef-bbf2-720771630604.jpg",
}

log = {
    "timestamp_inicio": datetime.now().isoformat(),
    "total": len(IMAGES_MAP),
    "downloaded": [],
    "failed": [],
    "total_bytes": 0
}

print(f"\n{'='*70}")
print("BAIXANDO TODAS AS 100 IMAGENS DE ARTIGOS")
print(f"{'='*70}\n")

start_time = time.time()

for img_id in sorted(IMAGES_MAP.keys()):
    url = IMAGES_MAP[img_id]
    filename = f"{img_id:08d}.jpg"
    filepath = OUTPUT_DIR / filename

    print(f"[{img_id:3d}/100] Baixando {filename}... ", end="", flush=True)

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        size = len(response.content)
        log["total_bytes"] += size

        print(f"OK ({size:,} bytes)")
        log["downloaded"].append({
            "id": img_id,
            "filename": filename,
            "size": size,
            "url": url
        })

        # Mostrar progresso a cada 10 imagens
        if img_id % 10 == 0:
            elapsed = time.time() - start_time
            avg_time = elapsed / img_id
            remaining = (100 - img_id) * avg_time
            print(f"  → Progresso: {img_id}% | Tempo decorrido: {elapsed:.1f}s | Estimado restante: {remaining:.1f}s")

    except Exception as e:
        print(f"ERRO: {e}")
        log["failed"].append({
            "id": img_id,
            "filename": filename,
            "error": str(e),
            "url": url
        })

elapsed_total = time.time() - start_time
log["timestamp_fim"] = datetime.now().isoformat()
log["tempo_total_segundos"] = elapsed_total

# Salvar log
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2, ensure_ascii=False)

print(f"\n{'='*70}")
print("RESUMO FINAL")
print(f"{'='*70}")
print(f"Total de imagens: {log['total']}")
print(f"Baixadas com sucesso: {len(log['downloaded'])}")
print(f"Falhas: {len(log['failed'])}")
print(f"Total de dados: {log['total_bytes']:,} bytes ({log['total_bytes']/1024/1024:.2f} MB)")
print(f"Tempo total: {elapsed_total:.1f} segundos ({elapsed_total/60:.1f} minutos)")
print(f"Custo total da geração: ${len(IMAGES_MAP) * 0.009:.2f} USD")
print(f"\nLog salvo em: {LOG_FILE}")
print(f"Imagens salvas em: {OUTPUT_DIR}")
print(f"{'='*70}\n")

if log["failed"]:
    print("FALHAS DETECTADAS:")
    for fail in log["failed"]:
        print(f"  - ID {fail['id']}: {fail['error']}")
else:
    print("SUCESSO TOTAL! Todas as 100 imagens foram baixadas!")
