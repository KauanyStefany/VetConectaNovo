#!/usr/bin/env python3
"""
Script para gerar TODAS as imagens restantes dos artigos.
Este script deve ser executado manualmente, chamando a ferramenta MCP para cada imagem.
"""

import json
import requests
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent
PROMPTS_FILE = BASE_DIR / "data" / "prompts_artigos.json"
OUTPUT_DIR = BASE_DIR / "static" / "img" / "artigos"
LOG_FILE = BASE_DIR / "data" / "log_geracao_artigos.json"

def load_prompts():
    """Carrega o arquivo de prompts."""
    with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_existing_images():
    """Retorna conjunto de imagens que já existem."""
    return {f.name for f in OUTPUT_DIR.glob('*.jpg')}

def download_image(url: str, filepath: Path) -> bool:
    """Baixa uma imagem da URL e salva no filepath."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        return True
    except Exception as e:
        print(f"  ❌ Erro ao baixar {filepath.name}: {e}")
        return False

def load_log():
    """Carrega o log existente ou cria um novo."""
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_log(log_entries):
    """Salva o log."""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_entries, f, indent=2, ensure_ascii=False)

def process_generated_image(artigo_id, url, log_entries):
    """Processa uma imagem gerada (baixa e registra no log)."""
    artigos = load_prompts()
    artigo = next(a for a in artigos if a['id'] == artigo_id)

    filepath = OUTPUT_DIR / artigo['filename']

    print(f"[{artigo_id}/100] {artigo['titulo']}")

    if filepath.exists():
        print(f"  ⏭️  Já existe: {artigo['filename']}")
        return True

    print(f"  ⬇️  Baixando de {url[:50]}...")

    if download_image(url, filepath):
        print(f"  ✅ Salvo: {artigo['filename']}")

        log_entries.append({
            "id": artigo_id,
            "titulo": artigo['titulo'],
            "filename": artigo['filename'],
            "url": url,
            "status": "success",
            "generated_at": datetime.now().isoformat()
        })
        return True
    else:
        log_entries.append({
            "id": artigo_id,
            "titulo": artigo['titulo'],
            "filename": artigo['filename'],
            "url": url,
            "status": "failed",
            "generated_at": datetime.now().isoformat()
        })
        return False

def main():
    """Função principal."""
    print("="*60)
    print("PROCESSADOR DE IMAGENS GERADAS")
    print("="*60)

    # Load data
    artigos = load_prompts()
    existing = get_existing_images()
    log_entries = load_log()

    print(f"\n📊 Status:")
    print(f"   Total de artigos: {len(artigos)}")
    print(f"   Imagens existentes: {len(existing)}")
    print(f"   Imagens pendentes: {len(artigos) - len(existing)}")
    print(f"   Entradas no log: {len(log_entries)}")

    # Imagens geradas manualmente (adicionar aqui conforme vão sendo geradas)
    # IDs 52-56 (continuação do lote anterior)
    manual_images = [
        (52, "https://im.runware.ai/image/ws/2/ii/54b15ed6-f3c2-425f-aa95-63938c3f3333.jpg"),
        (53, "https://im.runware.ai/image/ws/2/ii/e16d712f-0017-471a-804d-2e4caf7ef56b.jpg"),
        (54, "https://im.runware.ai/image/ws/2/ii/aded3abb-0c0c-44b8-b25c-b53b6dbdc93c.jpg"),
        (55, "https://im.runware.ai/image/ws/2/ii/038cb9e4-1274-4b16-ae7c-4fd6c2e48b17.jpg"),
        (56, "https://im.runware.ai/image/ws/2/ii/ae1c4b5f-0801-4c5a-8888-e495f9d5a97a.jpg"),
    ]

    print(f"\n🎨 Processando {len(manual_images)} imagens geradas...")

    success_count = 0
    for artigo_id, url in manual_images:
        if process_generated_image(artigo_id, url, log_entries):
            success_count += 1

    # Save log
    save_log(log_entries)

    print(f"\n✅ Processamento concluído!")
    print(f"   Baixadas com sucesso: {success_count}/{len(manual_images)}")
    print(f"   Log salvo em: {LOG_FILE}")

    # Mostrar pendentes
    existing_after = get_existing_images()
    pending_count = len(artigos) - len(existing_after)

    if pending_count > 0:
        print(f"\n⏳ Ainda faltam {pending_count} imagens para gerar")
        pending = [a for a in artigos if a['filename'] not in existing_after]
        print(f"   Próximas: {pending[0]['id']} a {min(pending[0]['id'] + 9, 100)}")

if __name__ == "__main__":
    main()
