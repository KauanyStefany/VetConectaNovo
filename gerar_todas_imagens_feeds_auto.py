#!/usr/bin/env python3
"""
Script automatizado para gerar TODAS as imagens dos feeds restantes
Este script gera um arquivo JSON com todos os prompts necessários
"""

import json
from pathlib import Path


def criar_prompt_inteligente(descricao):
    """
    Cria um prompt fotorealista otimizado baseado na descrição
    """
    descricao_lower = descricao.lower()

    # Identificar contexto e criar prompt específico
    base_prompt = f"Photorealistic image: {descricao}. "

    # Adicionar detalhes baseados em palavras-chave
    if any(word in descricao_lower for word in ['cachorro', 'cão', 'dog', 'labrador', 'golden', 'beagle', 'pastor', 'poodle', 'vira-lata', 'yorkshire', 'pug']):
        base_prompt += "Professional dog photography, sharp focus, detailed fur textures, expressive eyes, "
    elif any(word in descricao_lower for word in ['gato', 'cat', 'felino', 'gatinho', 'gata', 'siamês', 'siamese']):
        base_prompt += "Professional cat photography, sharp focus, detailed fur and whiskers, expressive eyes, "
    elif any(word in descricao_lower for word in ['hamster', 'roedor', 'porquinho', 'guinea pig']):
        base_prompt += "Professional small pet photography, sharp focus, detailed fur, cute expression, "
    elif any(word in descricao_lower for word in ['peixe', 'betta', 'aquário', 'neon']):
        base_prompt += "Professional aquarium photography, crystal clear water, sharp focus, vibrant colors, detailed fins and scales, "
    elif any(word in descricao_lower for word in ['pássaro', 'calopsita', 'ave', 'canário', 'bird']):
        base_prompt += "Professional bird photography, sharp focus, detailed feathers, vibrant colors, "
    elif any(word in descricao_lower for word in ['coelho', 'rabbit']):
        base_prompt += "Professional rabbit photography, sharp focus, detailed soft fur, cute expression, "
    elif any(word in descricao_lower for word in ['tartaruga', 'turtle', 'jabuti']):
        base_prompt += "Professional reptile photography, sharp focus, detailed shell texture, "
    elif any(word in descricao_lower for word in ['furão', 'ferret']):
        base_prompt += "Professional ferret photography, sharp focus, detailed fur, playful expression, "
    else:
        base_prompt += "Professional pet photography, sharp focus, detailed textures, "

    # Adicionar qualidade final
    base_prompt += "natural colors, warm and inviting atmosphere, high resolution DSLR quality, bokeh background"

    return base_prompt


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

    print(f"Total de feeds: {len(feeds)}")
    print(f"Imagens existentes: {len(existing_ids)}")
    print(f"Feeds para gerar: {len(feeds_to_generate)}")
    print()

    # Criar lista de prompts
    prompts_data = []

    for feed in feeds_to_generate:
        feed_id = feed['id_postagem_feed']
        descricao = feed['descricao']
        prompt = criar_prompt_inteligente(descricao)
        filename = f"{feed_id:08d}.jpg"

        prompts_data.append({
            "id": feed_id,
            "descricao": descricao,
            "prompt": prompt,
            "filename": filename,
            "url_destino": f"static/img/feeds/{filename}"
        })

    # Salvar em arquivo JSON
    output_file = Path('data/prompts_feeds_pendentes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(prompts_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Arquivo gerado: {output_file}")
    print(f"✓ Total de prompts: {len(prompts_data)}")
    print()
    print("Para processar todas as imagens:")
    print("1. Use este arquivo JSON para gerar cada imagem via MCP")
    print("2. Ou execute o script de geração batch que usa este JSON")
    print()

    # Mostrar primeiros 5 exemplos
    print("Primeiros 5 feeds a processar:")
    print("=" * 80)
    for item in prompts_data[:5]:
        print(f"\nID: {item['id']}")
        print(f"Arquivo: {item['filename']}")
        print(f"Descrição: {item['descricao']}")
        print(f"Prompt: {item['prompt'][:100]}...")


if __name__ == "__main__":
    main()
