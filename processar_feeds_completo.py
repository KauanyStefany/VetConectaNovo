#!/usr/bin/env python3
"""
Script para processar todos os feeds restantes e gerar lista de comandos
para o Claude executar via MCP
"""

import json
from pathlib import Path


def criar_prompt_fotorealista(descricao):
    """
    Cria um prompt fotorealista baseado na descrição do feed
    """
    # Palavras-chave para identificar o tipo de animal/situação
    descricao_lower = descricao.lower()

    # Mapeamento de contextos
    if any(word in descricao_lower for word in ['cachorro', 'cão', 'dog', 'labrador', 'golden', 'beagle', 'pastor', 'poodle', 'vira-lata']):
        tipo = 'dog'
    elif any(word in descricao_lower for word in ['gato', 'cat', 'felino', 'gatinho', 'gata']):
        tipo = 'cat'
    elif any(word in descricao_lower for word in ['hamster', 'roedor']):
        tipo = 'hamster'
    elif any(word in descricao_lower for word in ['porquinho', 'guinea pig', 'porquinho da índia']):
        tipo = 'guinea pig'
    elif any(word in descricao_lower for word in ['peixe', 'betta', 'aquário']):
        tipo = 'fish'
    elif any(word in descricao_lower for word in ['pássaro', 'calopsita', 'ave', 'bird']):
        tipo = 'bird'
    elif any(word in descricao_lower for word in ['coelho', 'rabbit']):
        tipo = 'rabbit'
    elif any(word in descricao_lower for word in ['tartaruga', 'turtle']):
        tipo = 'turtle'
    else:
        tipo = 'pet'

    # Criar prompt base
    prompt = f"Photorealistic image: {descricao}. "
    prompt += f"Professional {tipo} photography, sharp focus, detailed textures, "
    prompt += "natural colors, high resolution DSLR quality, warm and inviting atmosphere, bokeh background"

    return prompt


def main():
    # Carregar dados dos feeds
    json_path = Path('data/postagens_feeds.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        feeds = json.load(f)

    # Verificar imagens existentes
    img_dir = Path('static/img/feeds')
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

    print(f"# FEEDS PARA PROCESSAR: {len(feeds_to_generate)}")
    print(f"# Imagens já existentes: {len(existing_ids)}")
    print()

    # Gerar lista de comandos
    for idx, feed in enumerate(feeds_to_generate, 1):
        feed_id = feed['id_postagem_feed']
        descricao = feed['descricao']
        filename = f"{feed_id:08d}.jpg"
        prompt = criar_prompt_fotorealista(descricao)

        print(f"# [{idx}/{len(feeds_to_generate)}] Feed ID: {feed_id}")
        print(f"# Descrição: {descricao}")
        print(f"# Arquivo: {filename}")
        print(f"PROMPT: {prompt}")
        print()

        # A cada 20 feeds, adicionar separador
        if idx % 20 == 0:
            print("=" * 80)
            print(f"# CHECKPOINT: {idx} feeds processados")
            print("=" * 80)
            print()


if __name__ == "__main__":
    main()
