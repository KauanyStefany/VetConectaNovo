#!/usr/bin/env python3
"""
Script para gerar imagens de artigos usando a API Runware via MCP.
Processa 100 artigos, verifica imagens existentes e gera apenas as faltantes.
"""

import json
import os
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


# Configurações
BASE_DIR = Path("/Volumes/Externo/Ifes/VetConectaNovo")
PROMPTS_FILE = BASE_DIR / "data" / "prompts_artigos.json"
OUTPUT_DIR = BASE_DIR / "static" / "img" / "artigos"
LOG_FILE = BASE_DIR / "data" / "log_geracao_imagens_completo.json"

# Parâmetros da geração
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 768
COST_PER_IMAGE = 0.009  # USD


class ImageGenerator:
    """Gerenciador de geração de imagens."""

    def __init__(self):
        self.stats = {
            "total": 0,
            "generated": 0,
            "existing": 0,
            "failed": 0,
            "start_time": datetime.now().isoformat(),
            "details": []
        }

        # Garantir que diretório de saída existe
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def load_prompts(self) -> List[Dict[str, Any]]:
        """Carrega os prompts do arquivo JSON."""
        with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def image_exists(self, filename: str) -> bool:
        """Verifica se a imagem já existe."""
        return (OUTPUT_DIR / filename).exists()

    def download_image(self, url: str, filepath: Path) -> bool:
        """Baixa a imagem da URL e salva no arquivo."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                f.write(response.content)

            return True
        except Exception as e:
            print(f"  ⚠️  Erro ao baixar imagem: {e}")
            return False

    def generate_image(self, artigo: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera uma imagem para o artigo.
        NOTA: Esta função precisa ser chamada via MCP tool mcp__runware__generate_image
        """
        result = {
            "id": artigo["id"],
            "filename": artigo["filename"],
            "status": "pending",
            "timestamp": datetime.now().isoformat()
        }

        filepath = OUTPUT_DIR / artigo["filename"]

        # Verificar se já existe
        if self.image_exists(artigo["filename"]):
            result["status"] = "existing"
            self.stats["existing"] += 1
            print(f"  ✓ Imagem já existe: {artigo['filename']}")
            return result

        print(f"  → Gerando imagem {artigo['id']}: {artigo['titulo'][:50]}...")
        print(f"     Prompt: {artigo['prompt'][:80]}...")

        # Aqui seria a chamada para a ferramenta MCP
        # Por enquanto, retorna o status para processamento externo
        result["status"] = "needs_generation"
        result["prompt"] = artigo["prompt"]

        return result

    def process_all(self) -> Dict[str, Any]:
        """Processa todos os artigos."""
        artigos = self.load_prompts()
        self.stats["total"] = len(artigos)

        print(f"\n{'='*70}")
        print(f"INICIANDO GERAÇÃO DE IMAGENS DE ARTIGOS")
        print(f"{'='*70}")
        print(f"Total de artigos: {self.stats['total']}")
        print(f"Diretório de saída: {OUTPUT_DIR}")
        print(f"{'='*70}\n")

        to_generate = []

        for i, artigo in enumerate(artigos, 1):
            print(f"\n[{i}/{self.stats['total']}] Processando artigo {artigo['id']}...")

            result = self.generate_image(artigo)
            self.stats["details"].append(result)

            if result["status"] == "needs_generation":
                to_generate.append(artigo)

            # Mostrar progresso a cada 10 artigos
            if i % 10 == 0:
                print(f"\n{'─'*70}")
                print(f"PROGRESSO: {i}/{self.stats['total']} artigos processados")
                print(f"  • Já existentes: {self.stats['existing']}")
                print(f"  • A gerar: {len(to_generate)}")
                print(f"{'─'*70}\n")

        # Salvar lista de imagens a gerar
        if to_generate:
            to_generate_file = BASE_DIR / "data" / "artigos_a_gerar.json"
            with open(to_generate_file, 'w', encoding='utf-8') as f:
                json.dump(to_generate, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Lista de imagens a gerar salva em: {to_generate_file}")

        return to_generate

    def save_log(self):
        """Salva o log de processamento."""
        self.stats["end_time"] = datetime.now().isoformat()
        self.stats["cost_estimate_usd"] = self.stats["generated"] * COST_PER_IMAGE

        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Log salvo em: {LOG_FILE}")

    def print_summary(self, to_generate: List[Dict[str, Any]]):
        """Imprime o resumo final."""
        print(f"\n{'='*70}")
        print(f"RESUMO DO PROCESSAMENTO")
        print(f"{'='*70}")
        print(f"Total de artigos processados: {self.stats['total']}")
        print(f"Imagens já existentes: {self.stats['existing']}")
        print(f"Imagens a gerar: {len(to_generate)}")
        print(f"Imagens geradas: {self.stats['generated']}")
        print(f"Falhas: {self.stats['failed']}")
        print(f"\nCusto estimado: ${len(to_generate) * COST_PER_IMAGE:.2f} USD")
        print(f"{'='*70}\n")


def main():
    """Função principal."""
    generator = ImageGenerator()

    try:
        to_generate = generator.process_all()
        generator.save_log()
        generator.print_summary(to_generate)

        if to_generate:
            print(f"\n⚠️  ATENÇÃO: {len(to_generate)} imagens precisam ser geradas.")
            print(f"Execute a próxima etapa para gerar as imagens faltantes.")
            print(f"Arquivo: data/artigos_a_gerar.json\n")
        else:
            print(f"\n✓ Todas as imagens já existem! Nada a fazer.\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Processamento interrompido pelo usuário.")
        generator.save_log()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        generator.save_log()


if __name__ == "__main__":
    main()
