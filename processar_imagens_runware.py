#!/usr/bin/env python3
"""
Script para processar imagens dos feeds usando Runware AI
Este script deve ser chamado pelo Claude Code usando MCP tools
"""

import json
import sys
from pathlib import Path


def main():
    """Função principal que retorna os dados para processamento"""
    # Carregar prompts
    prompts_file = Path('data/prompts_feeds_pendentes.json')

    if not prompts_file.exists():
        print("ERRO: Arquivo de prompts não encontrado!")
        print("Execute primeiro: python gerar_todas_imagens_feeds_auto.py")
        sys.exit(1)

    with open(prompts_file, 'r', encoding='utf-8') as f:
        prompts_data = json.load(f)

    print(f"Total de imagens a processar: {len(prompts_data)}")
    print()

    # Criar diretório se não existir
    img_dir = Path('static/img/feeds')
    img_dir.mkdir(parents=True, exist_ok=True)

    # Retornar dados para processamento
    print("DADOS PARA PROCESSAMENTO:")
    print("=" * 80)

    for idx, item in enumerate(prompts_data, 1):
        print(f"\n[{idx}/{len(prompts_data)}]")
        print(f"ID: {item['id']}")
        print(f"Arquivo: {item['filename']}")
        print(f"Caminho: {item['url_destino']}")
        print(f"Prompt: {item['prompt']}")
        print("-" * 80)

    # Salvar também em formato processável
    output_file = Path('data/batch_processing_queue.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(prompts_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Fila de processamento salva em: {output_file}")
    print(f"✓ Total de imagens: {len(prompts_data)}")
    print()
    print("PRÓXIMO PASSO:")
    print("Use Claude Code MCP para gerar cada imagem chamando:")
    print("mcp__runware__generate_image com os prompts acima")


if __name__ == "__main__":
    main()
