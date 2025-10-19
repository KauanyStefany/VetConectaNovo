#!/usr/bin/env python3
"""
Script para coordenar a geração de imagens via Claude Code MCP.
Este script será executado pelo Claude usando a ferramenta mcp__runware__generate_image.
"""

import json
from pathlib import Path

BASE_DIR = Path("/Volumes/Externo/Ifes/VetConectaNovo")
INPUT_FILE = BASE_DIR / "data" / "artigos_a_gerar.json"
OUTPUT_DIR = BASE_DIR / "static" / "img" / "artigos"

def load_articles_to_generate():
    """Carrega a lista de artigos que precisam de imagens."""
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    """Função principal - coordena o processo."""
    articles = load_articles_to_generate()

    print(f"\n{'='*70}")
    print(f"ARTIGOS PARA GERAÇÃO")
    print(f"{'='*70}")
    print(f"Total: {len(articles)} imagens")
    print(f"Custo estimado: ${len(articles) * 0.009:.2f} USD")
    print(f"{'='*70}\n")

    # Mostrar os primeiros 10 para confirmação
    print("Primeiras 10 imagens:")
    for i, article in enumerate(articles[:10], 1):
        print(f"  {i}. [{article['id']:03d}] {article['titulo']}")

    if len(articles) > 10:
        print(f"  ... e mais {len(articles) - 10} artigos\n")

    print("\nEste arquivo serve como base para o Claude processar as gerações.")
    print("O Claude usará a ferramenta mcp__runware__generate_image para cada artigo.")

    return articles

if __name__ == "__main__":
    articles = main()
    print(f"\n✓ {len(articles)} artigos prontos para processamento\n")
