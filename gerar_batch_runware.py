#!/usr/bin/env python3
"""
Script para gerar imagens em lotes usando Runware AI
O Claude Code irá chamar os MCPs e este script gerencia o processo
"""

import json
import sys
import urllib.request
from pathlib import Path


def download_image(url, filepath):
    """Baixa uma imagem de uma URL e salva no caminho especificado"""
    try:
        urllib.request.urlretrieve(url, filepath)
        return True
    except Exception as e:
        print(f"ERRO ao baixar imagem: {e}")
        return False


def main():
    # Verificar argumentos
    if len(sys.argv) < 3:
        print("Uso: python gerar_batch_runware.py <image_url> <feed_id>")
        print("Exemplo: python gerar_batch_runware.py https://... 181")
        sys.exit(1)

    image_url = sys.argv[1]
    feed_id = int(sys.argv[2])

    # Gerar nome do arquivo e caminho
    filename = f"{feed_id:08d}.jpg"
    filepath = Path(f"static/img/feeds/{filename}")

    # Criar diretório se não existir
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Baixar imagem
    print(f"Baixando imagem do feed {feed_id}...")
    print(f"URL: {image_url}")
    print(f"Destino: {filepath}")

    if download_image(image_url, filepath):
        print(f"✓ Imagem salva com sucesso: {filepath}")
        return 0
    else:
        print(f"✗ Falha ao salvar imagem")
        return 1


if __name__ == "__main__":
    sys.exit(main())
