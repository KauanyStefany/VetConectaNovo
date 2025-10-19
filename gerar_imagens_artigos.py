#!/usr/bin/env python3
"""
Script para gerar imagens contextualizadas para artigos usando Runware AI.
Lê os artigos de data/postagens_artigos.json e gera imagens salvas em static/img/artigos/
"""

import json
import os
import sys
import time
import requests
from pathlib import Path

# Adicionar o diretório raiz ao path para importar módulos do projeto
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Importar as ferramentas do MCP já configuradas
# Nota: Como estamos usando o Claude Code com MCP, vamos simular chamadas
# Na prática, você vai usar as ferramentas MCP diretamente

def criar_prompt_imagem(titulo: str, conteudo: str, categoria: str) -> str:
    """Cria um prompt otimizado para geração de imagem baseado no artigo."""

    # Extrair as primeiras palavras-chave do título
    keywords = titulo.lower()

    # Mapear categorias para contextos visuais
    contextos = {
        "caninos": "professional veterinary photo of dogs",
        "felinos": "professional veterinary photo of cats",
        "roedores": "professional veterinary photo of rodents",
        "aves": "professional veterinary photo of birds",
        "répteis": "professional veterinary photo of reptiles",
        "peixes": "professional veterinary photo of fish in aquarium"
    }

    contexto_categoria = contextos.get(categoria.lower(), "professional veterinary photo")

    # Criar prompt contextualizado
    prompt = f"{contexto_categoria}, {keywords}, veterinary clinic setting, high quality, professional photography, clean background, natural lighting"

    return prompt[:500]  # Limitar tamanho do prompt


def baixar_e_salvar_imagem(url: str, caminho_destino: str) -> bool:
    """Baixa uma imagem da URL e salva no caminho especificado."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(caminho_destino, 'wb') as f:
            f.write(response.content)

        print(f"✓ Imagem salva: {caminho_destino}")
        return True
    except Exception as e:
        print(f"✗ Erro ao salvar imagem: {e}")
        return False


def main():
    # Caminhos
    json_path = BASE_DIR / "data" / "postagens_artigos.json"
    output_dir = BASE_DIR / "static" / "img" / "artigos"

    # Criar diretório se não existir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Ler artigos
    print(f"Lendo artigos de {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        artigos = json.load(f)

    print(f"Total de artigos: {len(artigos)}\n")

    # Mapear IDs de categorias para nomes
    categorias_map = {
        1: "Caninos",
        2: "Felinos",
        3: "Roedores",
        4: "Aves",
        5: "Répteis",
        6: "Peixes"
    }

    # Processar cada artigo
    total = len(artigos)
    for idx, artigo in enumerate(artigos, 1):
        id_artigo = artigo['id_postagem_artigo']
        titulo = artigo['titulo']
        conteudo = artigo['conteudo']
        id_categoria = artigo['id_categoria_artigo']
        categoria_nome = categorias_map.get(id_categoria, "Geral")

        # Nome do arquivo
        nome_arquivo = f"{id_artigo:08d}.jpg"
        caminho_completo = output_dir / nome_arquivo

        # Verificar se já existe
        if caminho_completo.exists():
            print(f"[{idx}/{total}] Pulando {nome_arquivo} - já existe")
            continue

        print(f"\n[{idx}/{total}] Processando: {titulo[:50]}...")
        print(f"  Categoria: {categoria_nome}")

        # Criar prompt
        prompt = criar_prompt_imagem(titulo, conteudo, categoria_nome)
        print(f"  Prompt: {prompt[:80]}...")

        # Este é um placeholder - a geração real será feita pelo Claude Code
        # usando a ferramenta mcp__runware__generate_image
        print(f"  AGUARDANDO: Gere a imagem usando mcp__runware__generate_image")
        print(f"  Prompt completo: {prompt}")
        print(f"  Salvar em: {caminho_completo}")
        print(f"  ---")

        # Pausa para não sobrecarregar a API
        time.sleep(1)

    print(f"\n✓ Script concluído!")
    print(f"  Total de artigos: {total}")
    print(f"  Diretório de saída: {output_dir}")


if __name__ == "__main__":
    main()
