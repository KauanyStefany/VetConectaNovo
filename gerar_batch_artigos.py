#!/usr/bin/env python3
"""
Script para gerar imagens de artigos em batch usando Runware AI.
Este script será executado pelo Claude Code com acesso às ferramentas MCP.
"""

import json
import requests
import time
from pathlib import Path

def baixar_imagem(url: str, caminho_destino: str) -> bool:
    """Baixa uma imagem da URL e salva no caminho especificado."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(caminho_destino, 'wb') as f:
            f.write(response.content)

        return True
    except Exception as e:
        print(f"✗ Erro ao baixar imagem: {e}")
        return False

def main():
    BASE_DIR = Path(__file__).resolve().parent

    # Ler prompts
    prompts_path = BASE_DIR / "data" / "prompts_artigos.json"
    with open(prompts_path, 'r', encoding='utf-8') as f:
        prompts_data = json.load(f)

    output_dir = BASE_DIR / "static" / "img" / "artigos"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Total de imagens a gerar: {len(prompts_data)}\n")

    # Criar arquivo de log
    log_path = BASE_DIR / "data" / "imagens_artigos_log.json"
    log_data = []

    for idx, item in enumerate(prompts_data, 1):
        artigo_id = item['id']
        filename = item['filename']
        prompt = item['prompt']
        titulo = item['titulo']

        caminho_destino = output_dir / filename

        # Pular se já existe
        if caminho_destino.exists():
            print(f"[{idx}/{len(prompts_data)}] ✓ Já existe: {filename}")
            continue

        print(f"\n[{idx}/{len(prompts_data)}] Gerando: {titulo[:50]}...")
        print(f"  Arquivo: {filename}")
        print(f"  Prompt: {prompt[:80]}...")

        # Esta linha será substituída pela chamada real à ferramenta MCP
        # quando executado pelo Claude Code
        print(f"  → USAR: mcp__runware__generate_image")
        print(f"     prompt: {prompt}")
        print(f"     width: 1024, height: 768")

        # Log
        log_data.append({
            'id': artigo_id,
            'filename': filename,
            'titulo': titulo,
            'prompt': prompt,
            'status': 'pending'
        })

        # Pausa para não sobrecarregar
        time.sleep(0.5)

    # Salvar log
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Log salvo em {log_path}")
    print(f"\nPara gerar as imagens, execute este script via Claude Code")
    print(f"que tem acesso à ferramenta mcp__runware__generate_image")

if __name__ == "__main__":
    main()
