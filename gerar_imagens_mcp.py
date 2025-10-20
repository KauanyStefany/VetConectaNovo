#!/usr/bin/env python3
"""
Script para gerar imagens usando MCP Runware.
Este script será executado pelo Claude Code que tem acesso ao MCP.
"""

import json
import os

# Configurações
OUTPUT_DIR = "static/img/artigos"
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 768
ARTIGOS_NOVOS_IDS = range(101, 149)  # IDs 101 a 148

# Prompts específicos para cada artigo
PROMPTS_ESPECIFICOS = {
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


def verificar_imagens_faltantes():
    """Verifica quais imagens precisam ser geradas."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    faltantes = []
    for id_artigo in ARTIGOS_NOVOS_IDS:
        output_filename = f"{id_artigo:08d}.jpg"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        if not os.path.exists(output_path):
            faltantes.append(id_artigo)

    return faltantes


def main():
    """Função principal."""
    print("=" * 80)
    print("VERIFICAÇÃO DE IMAGENS FALTANTES")
    print("=" * 80)
    print()

    faltantes = verificar_imagens_faltantes()

    print(f"✨ Total de artigos: {len(ARTIGOS_NOVOS_IDS)}")
    print(f"❌ Imagens faltantes: {len(faltantes)}")
    print(f"✅ Imagens já geradas: {len(ARTIGOS_NOVOS_IDS) - len(faltantes)}")
    print()

    if faltantes:
        print("📋 IDs que precisam de imagens:")
        print(faltantes)
        print()
        print("💡 Use o Claude Code para gerar essas imagens usando o MCP Runware")
    else:
        print("🎉 Todas as imagens já foram geradas!")

    # Salva lista de faltantes para referência
    with open("data/artigos_faltantes.json", "w", encoding="utf-8") as f:
        json.dump({
            "faltantes": faltantes,
            "prompts": {id: PROMPTS_ESPECIFICOS[id] for id in faltantes}
        }, f, ensure_ascii=False, indent=2)

    print(f"💾 Lista salva em: data/artigos_faltantes.json")


if __name__ == "__main__":
    main()
