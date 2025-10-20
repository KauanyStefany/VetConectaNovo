#!/usr/bin/env python3
"""
Lista todos os artigos que ainda não têm imagem gerada.
"""

import json
import os
from pathlib import Path

def main():
    # Carrega artigos
    with open('data/postagens_artigos.json', 'r', encoding='utf-8') as f:
        artigos = json.load(f)

    # Verifica quais não têm imagem
    sem_imagem = []
    com_imagem = []

    for artigo in artigos:
        id_artigo = artigo['id_postagem_artigo']
        arquivo = f"static/img/artigos/{id_artigo:08d}.jpg"

        if os.path.exists(arquivo):
            com_imagem.append(artigo)
        else:
            sem_imagem.append(artigo)

    print("=" * 80)
    print("RELATÓRIO DE IMAGENS DE ARTIGOS")
    print("=" * 80)
    print()
    print(f"✅ Artigos COM imagem: {len(com_imagem)}")
    print(f"❌ Artigos SEM imagem: {len(sem_imagem)}")
    print(f"📊 Total de artigos: {len(artigos)}")
    print()

    if sem_imagem:
        print("=" * 80)
        print("ARTIGOS QUE PRECISAM DE IMAGEM:")
        print("=" * 80)
        print()

        # Agrupa por categoria
        categorias = {}
        for artigo in sem_imagem:
            cat_id = artigo['id_categoria_artigo']
            if cat_id not in categorias:
                categorias[cat_id] = []
            categorias[cat_id].append(artigo)

        nomes_categorias = {
            1: "Cães",
            2: "Gatos",
            3: "Pequenos Mamíferos",
            4: "Aves",
            5: "Répteis",
            6: "Peixes"
        }

        for cat_id in sorted(categorias.keys()):
            artigos_cat = categorias[cat_id]
            nome_cat = nomes_categorias.get(cat_id, f"Categoria {cat_id}")

            print(f"\n📁 {nome_cat} ({len(artigos_cat)} artigos)")
            print("-" * 80)

            for artigo in artigos_cat:
                id_art = artigo['id_postagem_artigo']
                titulo = artigo['titulo']
                print(f"   [{id_art:3d}] {titulo}")

        print()
        print("=" * 80)
        print("PRÓXIMOS PASSOS:")
        print("=" * 80)
        print()
        print("1. Execute o script principal quando a API estiver disponível:")
        print("   python gerar_imagens_artigos.py")
        print()
        print("2. Ou gere imagens individuais com:")
        print("   python gerar_imagem_manual.py <ID>")
        print()
        print("3. Consulte os prompts em:")
        print("   data/prompts_imagens_artigos.json")
        print()
    else:
        print("🎉 Todos os artigos já possuem imagens!")


if __name__ == "__main__":
    main()
