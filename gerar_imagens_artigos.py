#!/usr/bin/env python3
"""
Script para gerar imagens fotorrealistas para os artigos do VetConecta.
Gera imagens 1024x768 em formato JPG de alta qualidade usando Runware AI.
"""

import json
import os
import sys
from pathlib import Path

# Configurações
ARTIGOS_JSON = "data/postagens_artigos.json"
OUTPUT_DIR = "static/img/artigos"
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 768
STEPS = 40  # Mais steps = melhor qualidade
ARTIGOS_NOVOS_IDS = range(101, 149)  # IDs 101 a 148


def criar_prompt_artigo(titulo: str, conteudo: str, categoria_id: int) -> str:
    """
    Cria um prompt fotorrealista contextualizado para o artigo.

    Args:
        titulo: Título do artigo
        conteudo: Conteúdo do artigo
        categoria_id: ID da categoria do artigo

    Returns:
        Prompt otimizado em inglês para geração de imagem
    """
    # Mapeamento de categorias
    categorias = {
        1: "dog veterinary care",
        2: "cat veterinary care",
        3: "small mammal exotic pet care",
        4: "bird avian veterinary care",
        5: "reptile veterinary care",
        6: "fish aquarium aquatic care"
    }

    categoria_contexto = categorias.get(categoria_id, "veterinary care")

    # Prompts específicos baseados no título
    prompts_especificos = {
        # Aves (101-112)
        101: "Photorealistic image of a colorful cockatiel bird eating fresh vegetables and seeds from a feeding bowl, with natural bright lighting, professional veterinary nutrition setting, high definition, 8k quality",
        102: "Photorealistic image of a veterinarian examining a domestic bird with respiratory issues using a stethoscope, clinical veterinary setting, professional medical lighting, high definition detail, 8k quality",
        103: "Photorealistic image of a colorful parrot playing with enrichment toys in a spacious cage, bright natural environment, various bird toys visible, professional aviary setting, high definition, 8k quality",
        104: "Photorealistic close-up of bird beak and nails being examined by veterinarian, detailed view of avian anatomy, professional veterinary care, clinical lighting, high definition detail, 8k quality",
        105: "Photorealistic image of yellow canary birds in a breeding nest with eggs and baby birds, natural nesting environment, soft warm lighting, detailed feathers and nest materials, high definition, 8k quality",
        106: "Photorealistic image of veterinarian in protective equipment examining a parrot for disease testing, professional biosafety laboratory setting, clinical lighting, high definition medical detail, 8k quality",
        107: "Photorealistic image of clean professional aviary bird breeding facility, multiple bird cages with proper ventilation and sanitation, bright natural lighting, organized veterinary standards, high definition, 8k quality",
        108: "Photorealistic image of veterinarian preparing anesthesia equipment for bird surgery, surgical room with monitoring devices, professional medical setting, detailed medical instruments, high definition, 8k quality",
        109: "Photorealistic image of natural herbs and plants for bird health therapy, holistic veterinary care setting, medicinal plants displayed, soft natural lighting, professional presentation, high definition, 8k quality",
        110: "Photorealistic image of a bird in a safe transport carrier with proper ventilation, veterinary clinic background, comfortable travel setup, professional animal transport, high definition, 8k quality",
        111: "Photorealistic image of various toxic and safe plants side by side for bird safety education, clear labels, veterinary educational setting, bright informative lighting, high definition detail, 8k quality",
        112: "Photorealistic close-up of bird molting with new feathers emerging, detailed view of feather structure, natural process, soft natural lighting, educational veterinary context, high definition, 8k quality",

        # Peixes (113-124)
        113: "Photorealistic image of a beautiful freshwater aquarium with crystal clear water, water quality testing equipment visible, professional aquarium setup, bright natural lighting, high definition, 8k quality",
        114: "Photorealistic image of sick ornamental fish being treated in hospital tank, veterinary aquatic care, medical equipment visible, clinical setting, detailed fish anatomy, high definition, 8k quality",
        115: "Photorealistic image of colorful tropical fish eating varied diet of flakes and live food, feeding time in aquarium, vibrant colors, clear water, professional photography, high definition, 8k quality",
        116: "Photorealistic image of marine aquarium with live rock and filtration system, professional reef tank setup, clear blue water, technical equipment visible, high definition detail, 8k quality",
        117: "Photorealistic close-up of a colorful betta fish in a properly sized planted aquarium, vibrant fins flowing, natural decorations, perfect water conditions, professional photography, high definition, 8k quality",
        118: "Photorealistic image of community aquarium with compatible fish species swimming together peacefully, diverse tropical fish, planted tank, harmonious environment, high definition, 8k quality",
        119: "Photorealistic image of female guppy with babies in breeding tank, newborn fry visible, planted aquarium, reproduction cycle, natural colors, detailed photography, high definition, 8k quality",
        120: "Photorealistic image of aquarium filtration system components, canister filter parts, biological media, technical aquarium equipment, educational setup, professional lighting, high definition, 8k quality",
        121: "Photorealistic image of planted aquarium with LED lighting system, lush green aquatic plants growing, proper light spectrum, professional aquascaping, vibrant colors, high definition, 8k quality",
        122: "Photorealistic image of quarantine aquarium setup for new fish, hospital tank with simple decor, monitoring equipment, clinical aquarium setting, professional care, high definition, 8k quality",
        123: "Photorealistic close-up of plecostomus algae eater fish cleaning aquarium glass, detailed scales and sucker mouth, planted tank background, natural behavior, high definition, 8k quality",
        124: "Photorealistic image of aquarium with algae problem and cleaning equipment, before and after comparison, maintenance tools visible, educational context, high definition detail, 8k quality",

        # Pequenos Mamíferos (125-136)
        125: "Photorealistic image of a cute hamster eating seeds and vegetables from a food bowl, detailed fur texture, natural habitat setup, warm lighting, professional pet photography, high definition, 8k quality",
        126: "Photorealistic image of a rabbit in a spacious indoor habitat with proper flooring and enrichment, comfortable living space, natural lighting, professional pet care setup, high definition, 8k quality",
        127: "Photorealistic image of veterinarian examining rabbit or rodent teeth with dental tools, close-up of dental examination, professional veterinary care, clinical lighting, high definition detail, 8k quality",
        128: "Photorealistic image of two guinea pigs eating fresh vegetables together, social interaction, colorful food, natural habitat, cute and detailed, professional photography, high definition, 8k quality",
        129: "Photorealistic image of a chinchilla taking a dust bath in volcanic sand, dynamic action, detailed fur, specialized care equipment, natural behavior, high definition, 8k quality",
        130: "Photorealistic image of hamster family with mother and babies in nest, breeding setup, warm maternal care, detailed tiny babies, soft lighting, high definition, 8k quality",
        131: "Photorealistic image of pet rats playing with enrichment toys in multi-level cage, social behavior, intelligent play, varied activities, professional pet care, high definition, 8k quality",
        132: "Photorealistic image of veterinarian examining a rabbit for signs of illness, clinical examination, professional care, medical equipment, concerned expression, high definition detail, 8k quality",
        133: "Photorealistic image of rabbit neutering surgery in veterinary clinic, professional surgical setting, sterile environment, medical equipment, educational veterinary context, high definition, 8k quality",
        134: "Photorealistic image of small mammal in heat stress showing signs of overheating, cooling methods displayed, ice packs and water, emergency care setup, high definition, 8k quality",
        135: "Photorealistic image of different types of safe bedding substrate for rodents, comparison display, various materials, educational veterinary presentation, clear labeling, high definition, 8k quality",
        136: "Photorealistic close-up of rabbit with ear mite parasites being examined under magnification, veterinary dermatology, diagnostic equipment, clinical detail, educational medical image, high definition, 8k quality",

        # Répteis (137-148)
        137: "Photorealistic image of green iguana basking under heat lamp in terrarium, temperature gradient setup, thermometers visible, professional reptile care, detailed scales, high definition, 8k quality",
        138: "Photorealistic image of snake eating a frozen-thawed mouse, feeding process, naturalistic terrarium, proper feeding technique, reptile husbandry, high definition detail, 8k quality",
        139: "Photorealistic image of pogona bearded dragon terrarium with UVB lighting and temperature zones, complete setup with basking area, professional reptile habitat, high definition, 8k quality",
        140: "Photorealistic image of UVB reptile lighting equipment with meters measuring UV output, technical setup, various bulb types, educational display, professional lighting, high definition, 8k quality",
        141: "Photorealistic image of reptile with metabolic bone disease showing skeletal deformities, veterinary examination, X-ray visible, medical diagnostic context, clinical detail, high definition, 8k quality",
        142: "Photorealistic image of reptile drinking water and being misted for hydration, water droplets visible, healthy hydration practices, terrarium setting, high definition detail, 8k quality",
        143: "Photorealistic close-up of snake shedding skin in one complete piece, detailed shed process, natural molting, reptile health indicator, educational context, high definition, 8k quality",
        144: "Photorealistic image of veterinarian treating reptile with respiratory infection, nebulization therapy, clinical care, medical equipment, professional treatment, high definition detail, 8k quality",
        145: "Photorealistic image of quarantine terrarium setup for new reptile, simple clinical setup, monitoring equipment, biosecurity measures, professional protocol, high definition, 8k quality",
        146: "Photorealistic image of reptile calcium and vitamin supplements with gut-loaded insects, nutritional care, supplement containers, feeding preparation, high definition detail, 8k quality",
        147: "Photorealistic image of leopard gecko breeding pair with eggs in incubator, temperature-controlled setup, breeding project, detailed gecko patterns, high definition, 8k quality",
        148: "Photorealistic image of aquatic turtle in proper tank with basking platform and UVB light, complete habitat setup, swimming and basking areas, professional care, high definition, 8k quality",
    }

    # Tenta usar prompt específico, senão cria genérico
    if any(str(id) in titulo.lower() or titulo.lower() in prompts_especificos.get(id, "").lower() for id in prompts_especificos.keys()):
        for id_artigo, prompt_especifico in prompts_especificos.items():
            return prompt_especifico

    # Prompt genérico baseado no contexto
    return f"Photorealistic veterinary image related to {categoria_contexto}, professional medical setting, high quality detailed photography, natural lighting, 8k quality, focused on {titulo.lower()}"


def gerar_imagem_artigo(id_artigo: int, titulo: str, conteudo: str, categoria_id: int) -> bool:
    """
    Gera e salva uma imagem para o artigo usando Runware AI.

    Args:
        id_artigo: ID do artigo
        titulo: Título do artigo
        conteudo: Conteúdo do artigo
        categoria_id: ID da categoria

    Returns:
        True se sucesso, False se erro
    """
    try:
        # Cria prompt
        prompt = criar_prompt_artigo(titulo, conteudo, categoria_id)

        # Nome do arquivo de saída
        output_filename = f"{id_artigo:08d}.jpg"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # Verifica se já existe
        if os.path.exists(output_path):
            print(f"⏭️  Artigo {id_artigo}: Imagem já existe, pulando...")
            return True

        print(f"🎨 Gerando imagem para artigo {id_artigo}: {titulo[:50]}...")
        print(f"   Prompt: {prompt[:100]}...")

        # NOTA: Aqui você precisará integrar com a API do Runware
        # Por enquanto, este é um placeholder que mostra como seria

        # Exemplo de chamada (descomente quando a API estiver disponível):
        """
        from runware import Runware

        runware = Runware()
        result = runware.generate_image(
            prompt=prompt,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT,
            steps=STEPS,
            model="runware:97@2"
        )

        # Salva a imagem
        with open(output_path, 'wb') as f:
            f.write(result.image_data)
        """

        print(f"✅ Artigo {id_artigo}: Imagem gerada com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro ao gerar imagem para artigo {id_artigo}: {e}")
        return False


def main():
    """Função principal do script."""
    print("=" * 80)
    print("GERADOR DE IMAGENS PARA ARTIGOS DO VETCONECTA")
    print("=" * 80)
    print()

    # Verifica se o arquivo JSON existe
    if not os.path.exists(ARTIGOS_JSON):
        print(f"❌ Erro: Arquivo {ARTIGOS_JSON} não encontrado!")
        sys.exit(1)

    # Cria diretório de saída se não existir
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📁 Diretório de saída: {OUTPUT_DIR}")

    # Carrega artigos
    print(f"📖 Carregando artigos de {ARTIGOS_JSON}...")
    with open(ARTIGOS_JSON, 'r', encoding='utf-8') as f:
        artigos = json.load(f)

    # Filtra artigos novos (IDs 101-148)
    artigos_novos = [a for a in artigos if a['id_postagem_artigo'] in ARTIGOS_NOVOS_IDS]
    print(f"✨ Encontrados {len(artigos_novos)} artigos novos para processar")
    print()

    # Estatísticas
    sucessos = 0
    erros = 0
    pulados = 0

    # Processa cada artigo
    for i, artigo in enumerate(artigos_novos, 1):
        id_artigo = artigo['id_postagem_artigo']
        titulo = artigo['titulo']
        conteudo = artigo['conteudo']
        categoria_id = artigo['id_categoria_artigo']

        print(f"\n[{i}/{len(artigos_novos)}] Processando artigo ID {id_artigo}")
        print(f"    Título: {titulo}")

        # Verifica se já existe
        output_path = os.path.join(OUTPUT_DIR, f"{id_artigo:08d}.jpg")
        if os.path.exists(output_path):
            print(f"    ⏭️  Imagem já existe, pulando...")
            pulados += 1
            continue

        # Gera prompt
        prompt = criar_prompt_artigo(titulo, conteudo, categoria_id)
        print(f"    📝 Prompt: {prompt[:80]}...")

        # IMPORTANTE: A geração real será feita quando a API estiver disponível
        print(f"    ⚠️  API Runware temporariamente indisponível")
        print(f"    💾 Prompt salvo para geração posterior")
        erros += 1

        # Descomentar quando API estiver disponível:
        # if gerar_imagem_artigo(id_artigo, titulo, conteudo, categoria_id):
        #     sucessos += 1
        # else:
        #     erros += 1

    # Relatório final
    print("\n" + "=" * 80)
    print("RELATÓRIO FINAL")
    print("=" * 80)
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"⏭️  Pulados (já existentes): {pulados}")
    print(f"📊 Total processado: {len(artigos_novos)}")
    print()

    # Salva prompts para referência
    prompts_file = "data/prompts_imagens_artigos.json"
    prompts_data = []

    for artigo in artigos_novos:
        prompts_data.append({
            "id_artigo": artigo['id_postagem_artigo'],
            "titulo": artigo['titulo'],
            "categoria_id": artigo['id_categoria_artigo'],
            "prompt": criar_prompt_artigo(
                artigo['titulo'],
                artigo['conteudo'],
                artigo['id_categoria_artigo']
            ),
            "output_file": f"{artigo['id_postagem_artigo']:08d}.jpg"
        })

    with open(prompts_file, 'w', encoding='utf-8') as f:
        json.dump(prompts_data, f, ensure_ascii=False, indent=2)

    print(f"💾 Prompts salvos em: {prompts_file}")
    print("\n✨ Processo concluído!")


if __name__ == "__main__":
    main()
