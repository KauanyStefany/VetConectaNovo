#!/usr/bin/env python3
"""
Script AUTOMATIZADO para gerar todas as imagens de artigos.
Este script será executado diretamente pelo Claude Code que tem acesso ao Runware.
"""

import json
import requests
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def baixar_imagem(url: str, destino: Path) -> bool:
    """Baixa imagem e salva."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(destino, 'wb') as f:
            f.write(response.content)

        return True
    except Exception as e:
        print(f"  ✗ Erro ao baixar: {e}")
        return False

def processar_artigos():
    """
    Processa todos os artigos pendentes.
    Este será executado com suporte do Claude Code para chamadas Runware.
    """

    # Ler lista de processamento
    pendentes_file = BASE_DIR / "data" / "processar_imagens_pendentes.json"
    with open(pendentes_file, 'r', encoding='utf-8') as f:
        pendentes = json.load(f)

    output_dir = BASE_DIR / "static" / "img" / "artigos"

    print(f"═══════════════════════════════════════════════════════")
    print(f" GERAÇÃO AUTOMÁTICA DE IMAGENS DE ARTIGOS")
    print(f"═══════════════════════════════════════════════════════")
    print(f"Total de imagens: {len(pendentes)}\n")

    sucesso = 0
    falhas = 0

    # Log de processamento
    log_file = BASE_DIR / "data" / "log_geracao_imagens.json"
    log_data = []

    for idx, item in enumerate(pendentes, 1):
        artigo_id = item['id']
        filename = item['filename']
        prompt = item['prompt']
        titulo = item['titulo']

        print(f"\n[{idx}/{len(pendentes)}] ID {artigo_id}: {titulo[:50]}...")

        # Verificar se já existe
        if Path(filename).exists():
            print(f"  ✓ Já existe, pulando...")
            sucesso += 1
            continue

        # AQUI: Chamada para Runware via MCP
        # Como este script é executado pelo Claude Code,
        # esta parte precisa ser substituída por uma chamada real
        print(f"  → Gerando imagem via Runware...")
        print(f"     Prompt: {prompt[:80]}...")

        # PLACEHOLDER: URL da imagem gerada
        # Em produção, isso virá da ferramenta MCP
        image_url = None  # Será preenchido pela ferramenta MCP

        if image_url:
            print(f"  → Baixando de {image_url}...")
            if baixar_imagem(image_url, Path(filename)):
                print(f"  ✓ Sucesso!")
                sucesso += 1

                log_data.append({
                    'id': artigo_id,
                    'filename': filename,
                    'status': 'success',
                    'url': image_url
                })
            else:
                print(f"  ✗ Falha no download")
                falhas += 1

                log_data.append({
                    'id': artigo_id,
                    'filename': filename,
                    'status': 'failed_download'
                })
        else:
            print(f"  ✗ Falha na geração")
            falhas += 1

            log_data.append({
                'id': artigo_id,
                'filename': filename,
                'status': 'failed_generation'
            })

    # Salvar log
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print(f"\n═══════════════════════════════════════════════════════")
    print(f" RESUMO")
    print(f"═══════════════════════════════════════════════════════")
    print(f"Total processado: {len(pendentes)}")
    print(f"Sucesso: {sucesso}")
    print(f"Falhas: {falhas}")
    print(f"\nLog salvo em: {log_file}")

if __name__ == "__main__":
    processar_artigos()
