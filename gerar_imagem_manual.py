#!/usr/bin/env python3
"""
Script auxiliar para gerar uma única imagem manualmente.
Útil para testar a API ou gerar imagens individualmente.

Uso:
    python gerar_imagem_manual.py <id_artigo>

Exemplo:
    python gerar_imagem_manual.py 101
"""

import json
import sys
import os

def carregar_prompt(id_artigo: int) -> dict:
    """Carrega o prompt do arquivo JSON."""
    with open('data/prompts_imagens_artigos.json', 'r', encoding='utf-8') as f:
        prompts = json.load(f)

    for item in prompts:
        if item['id_artigo'] == id_artigo:
            return item

    return None


def main():
    if len(sys.argv) < 2:
        print("Uso: python gerar_imagem_manual.py <id_artigo>")
        print("Exemplo: python gerar_imagem_manual.py 101")
        sys.exit(1)

    try:
        id_artigo = int(sys.argv[1])
    except ValueError:
        print("Erro: ID do artigo deve ser um número")
        sys.exit(1)

    # Carrega prompt
    item = carregar_prompt(id_artigo)

    if not item:
        print(f"Erro: Artigo {id_artigo} não encontrado")
        sys.exit(1)

    print("=" * 80)
    print(f"GERADOR MANUAL DE IMAGEM - Artigo {id_artigo}")
    print("=" * 80)
    print()
    print(f"📝 Título: {item['titulo']}")
    print(f"📂 Categoria: {item['categoria_id']}")
    print(f"💾 Arquivo: {item['output_file']}")
    print()
    print("🎨 PROMPT:")
    print("-" * 80)
    print(item['prompt'])
    print("-" * 80)
    print()

    # Aqui você pode adicionar o código para gerar a imagem
    # usando qualquer API de sua preferência

    print("⚠️  Para gerar a imagem, copie o prompt acima e use em:")
    print("   - DALL-E (https://openai.com/dall-e)")
    print("   - Midjourney (https://midjourney.com)")
    print("   - Stable Diffusion (https://stablediffusionweb.com)")
    print("   - Leonardo AI (https://leonardo.ai)")
    print()
    print(f"📁 Salve a imagem gerada como: static/img/artigos/{item['output_file']}")
    print()


if __name__ == "__main__":
    main()
