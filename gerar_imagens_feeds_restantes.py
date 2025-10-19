#!/usr/bin/env python3
"""
Script para gerar imagens dos feeds restantes (40-304)
usando Runware AI via MCP
"""

import json
import os
import sys
import time
from pathlib import Path

# Adicionar o diretório raiz ao path para importar módulos
sys.path.insert(0, str(Path(__file__).parent))


def load_feeds_data():
    """Carrega os dados dos feeds do arquivo JSON"""
    json_path = Path(__file__).parent / "data" / "postagens_feeds.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_existing_images():
    """Retorna o conjunto de IDs de feeds que já têm imagens"""
    img_dir = Path(__file__).parent / "static" / "img" / "feeds"
    if not img_dir.exists():
        return set()

    existing_ids = set()
    for img_file in img_dir.glob("*.jpg"):
        # Nome do arquivo é no formato 00000001.jpg
        try:
            feed_id = int(img_file.stem)
            existing_ids.add(feed_id)
        except ValueError:
            continue

    return existing_ids


def create_prompt_for_feed(feed):
    """
    Cria um prompt fotorealista para gerar imagem baseada na descrição do feed
    """
    descricao = feed['descricao']

    # Criar um prompt fotorealista detalhado
    prompt = f"""Photorealistic image: {descricao}.
High quality photograph, professional lighting, sharp focus, detailed textures,
natural colors, realistic pet photography, high resolution, DSLR quality,
bokeh background, warm and inviting atmosphere"""

    return prompt


def generate_image_filename(feed_id):
    """Gera o nome do arquivo no formato 00000001.jpg"""
    return f"{feed_id:08d}.jpg"


def main():
    """Função principal"""
    print("=" * 80)
    print("GERADOR DE IMAGENS PARA FEEDS")
    print("=" * 80)

    # Carregar dados
    print("\n[1/4] Carregando dados dos feeds...")
    feeds = load_feeds_data()
    print(f"   ✓ {len(feeds)} feeds encontrados no JSON")

    # Verificar imagens existentes
    print("\n[2/4] Verificando imagens existentes...")
    existing_ids = get_existing_images()
    print(f"   ✓ {len(existing_ids)} imagens já existem")

    # Filtrar feeds que precisam de imagens
    feeds_to_generate = [f for f in feeds if f['id_postagem_feed'] not in existing_ids]
    print(f"   ✓ {len(feeds_to_generate)} feeds precisam de imagens")

    if not feeds_to_generate:
        print("\n✓ Todas as imagens já foram geradas!")
        return

    # Mostrar feeds que serão processados
    print(f"\n[3/4] Feeds a processar:")
    print(f"   Primeiro: ID {feeds_to_generate[0]['id_postagem_feed']}")
    print(f"   Último: ID {feeds_to_generate[-1]['id_postagem_feed']}")

    # Criar diretório se não existir
    img_dir = Path(__file__).parent / "static" / "img" / "feeds"
    img_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[4/4] Iniciando geração de imagens...")
    print(f"   Diretório: {img_dir}")
    print("\n" + "=" * 80)

    # Processar cada feed
    success_count = 0
    error_count = 0

    for idx, feed in enumerate(feeds_to_generate, 1):
        feed_id = feed['id_postagem_feed']
        descricao = feed['descricao']

        print(f"\n[{idx}/{len(feeds_to_generate)}] Feed ID: {feed_id}")
        print(f"   Descrição: {descricao[:80]}{'...' if len(descricao) > 80 else ''}")

        # Criar prompt
        prompt = create_prompt_for_feed(feed)
        print(f"   Prompt criado ({len(prompt)} caracteres)")

        # Gerar nome do arquivo
        filename = generate_image_filename(feed_id)
        filepath = img_dir / filename

        print(f"   Arquivo: {filename}")
        print(f"   STATUS: Pronto para geração via MCP")
        print(f"   Prompt: {prompt[:100]}...")

        # NOTA: A geração real será feita manualmente via MCP
        # Este script apenas prepara os dados

    print("\n" + "=" * 80)
    print("SCRIPT CONCLUÍDO")
    print("=" * 80)
    print(f"\nEstatísticas:")
    print(f"   Total de feeds: {len(feeds)}")
    print(f"   Imagens existentes: {len(existing_ids)}")
    print(f"   Feeds a processar: {len(feeds_to_generate)}")
    print(f"\nPróximos passos:")
    print(f"   1. Use o MCP tool 'mcp__runware__generate_image' para cada feed")
    print(f"   2. Salve as imagens no diretório: {img_dir}")
    print(f"   3. Use o formato de nome: 00000XXX.jpg")
    print()


if __name__ == "__main__":
    main()
