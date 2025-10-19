#!/usr/bin/env python3
"""
Script para download de imagens após geração via Runware.
Este script recebe URLs de imagens e as baixa para o diretório correto.
"""

import json
import requests
import time
from pathlib import Path

def baixar_imagem(url: str, destino: str) -> bool:
    """Baixa imagem da URL e salva no destino."""
    try:
        print(f"  Baixando de {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(destino, 'wb') as f:
            f.write(response.content)

        tamanho = len(response.content) / 1024  # KB
        print(f"  ✓ Salvo: {destino} ({tamanho:.1f} KB)")
        return True

    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False

def main():
    # Este script será usado após a geração das imagens
    print("Script preparado para download de imagens em batch")
    print("Aguardando geração das imagens via Runware...")

if __name__ == "__main__":
    main()
