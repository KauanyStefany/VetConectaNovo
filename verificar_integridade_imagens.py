#!/usr/bin/env python3
"""
Script para verificar a integridade das imagens dos artigos.
Útil para garantir que todas as imagens estão corretas e acessíveis.
"""

import json
from pathlib import Path
from PIL import Image
import sys

def verificar_integridade():
    """Verifica se todas as imagens estão presentes e válidas."""

    print("=" * 80)
    print("VERIFICAÇÃO DE INTEGRIDADE - IMAGENS DOS ARTIGOS")
    print("=" * 80)
    print()

    # Paths
    output_dir = Path(__file__).parent / "static" / "img" / "artigos"
    prompts_file = Path(__file__).parent / "data" / "prompts_artigos.json"

    # Carregar prompts
    with open(prompts_file, 'r', encoding='utf-8') as f:
        artigos = json.load(f)

    # Estatísticas
    total = len(artigos)
    existentes = 0
    corrompidas = 0
    faltantes = []
    problemas = []

    print(f"Verificando {total} imagens...")
    print()

    for artigo in artigos:
        artigo_id = artigo['id']
        filename = artigo['filename']
        filepath = output_dir / filename

        # Verificar existência
        if not filepath.exists():
            faltantes.append(artigo_id)
            print(f"❌ [{artigo_id:03d}] FALTANDO: {filename}")
            continue

        # Verificar integridade (tentar abrir a imagem)
        try:
            with Image.open(filepath) as img:
                # Verificar dimensões
                width, height = img.size

                if width != 1024 or height != 768:
                    problemas.append({
                        'id': artigo_id,
                        'problema': f'Dimensões incorretas: {width}x{height} (esperado: 1024x768)',
                        'filename': filename
                    })
                    print(f"⚠️  [{artigo_id:03d}] DIMENSÃO: {width}x{height} - {filename}")
                else:
                    existentes += 1
                    if artigo_id % 20 == 0:  # Mostrar progresso a cada 20
                        print(f"✅ [{artigo_id:03d}] OK: {filename}")

        except Exception as e:
            corrompidas.append(artigo_id)
            problemas.append({
                'id': artigo_id,
                'problema': f'Erro ao abrir: {str(e)}',
                'filename': filename
            })
            print(f"💥 [{artigo_id:03d}] CORROMPIDA: {filename} - {e}")

    # Resumo
    print()
    print("=" * 80)
    print("RESUMO DA VERIFICAÇÃO")
    print("=" * 80)
    print()
    print(f"✅ Imagens OK:        {existentes}/{total} ({existentes/total*100:.1f}%)")
    print(f"❌ Faltantes:         {len(faltantes)}")
    print(f"💥 Corrompidas:       {len(corrompidas)}")
    print(f"⚠️  Com problemas:    {len(problemas)}")
    print()

    # Detalhes dos problemas
    if faltantes:
        print("IMAGENS FALTANTES:")
        print(f"  IDs: {faltantes}")
        print()

    if corrompidas:
        print("IMAGENS CORROMPIDAS:")
        print(f"  IDs: {corrompidas}")
        print()

    if problemas:
        print("PROBLEMAS DETECTADOS:")
        for p in problemas[:5]:  # Mostrar apenas os 5 primeiros
            print(f"  [{p['id']:03d}] {p['problema']}")
        if len(problemas) > 5:
            print(f"  ... e mais {len(problemas) - 5} problemas")
        print()

    # Resultado final
    if existentes == total and not problemas:
        print("🎉 TODAS AS IMAGENS ESTÃO OK!")
        return 0
    else:
        print("⚠️  EXISTEM PROBLEMAS QUE PRECISAM SER CORRIGIDOS")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(verificar_integridade())
    except Exception as e:
        print(f"❌ ERRO FATAL: {e}")
        sys.exit(1)
