#!/usr/bin/env python3
"""
Script para listar os feeds que precisam de imagens
Este script será usado pelo Claude para gerar as imagens via MCP
"""

import json
import os
from pathlib import Path


def main():
    # Carregar dados dos feeds
    json_path = Path(__file__).parent / "data" / "postagens_feeds.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        feeds = json.load(f)

    # Verificar imagens existentes
    img_dir = Path(__file__).parent / "static" / "img" / "feeds"
    existing_ids = set()

    if img_dir.exists():
        for img_file in img_dir.glob("*.jpg"):
            try:
                feed_id = int(img_file.stem)
                existing_ids.add(feed_id)
            except ValueError:
                continue

    # Filtrar feeds sem imagens
    feeds_to_generate = [f for f in feeds if f['id_postagem_feed'] not in existing_ids]

    print(f"Total de feeds: {len(feeds)}")
    print(f"Imagens existentes: {len(existing_ids)}")
    print(f"Feeds para gerar: {len(feeds_to_generate)}")
    print("\n" + "="*80 + "\n")

    # Exibir os feeds que precisam de imagens
    for feed in feeds_to_generate:
        feed_id = feed['id_postagem_feed']
        descricao = feed['descricao']
        filename = f"{feed_id:08d}.jpg"

        print(f"ID: {feed_id:3d} | Arquivo: {filename} | Descrição: {descricao}")
        print()


if __name__ == "__main__":
    main()
