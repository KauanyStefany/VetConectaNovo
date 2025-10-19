#!/usr/bin/env python3
"""
Script para processar e gerar imagens de artigos usando prompts estruturados.
Gera um arquivo JSON com os prompts que serão usados pelo Claude Code.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def criar_prompt_profissional(titulo: str, categoria_animal: str) -> str:
    """
    Cria prompts profissionais para geração de imagens veterinárias.
    """

    # Contextos por tipo de animal
    contextos = {
        'dogs': 'professional veterinary photograph of a dog',
        'cats': 'professional veterinary photograph of a cat',
        'rodents': 'professional veterinary photograph of a rodent (hamster, guinea pig, or rabbit)',
        'birds': 'professional veterinary photograph of a pet bird',
        'reptiles': 'professional veterinary photograph of a reptile (turtle, lizard, or snake)',
        'fish': 'professional veterinary photograph of colorful fish in aquarium'
    }

    base_context = contextos.get(categoria_animal, 'professional veterinary photograph of pet animal')

    # Adicionar contexto do título
    titulo_lower = titulo.lower()

    # Palavras-chave para diferentes tipos de imagens
    if any(word in titulo_lower for word in ['filhote', 'puppy', 'kitten', 'bebê']):
        age_context = 'young, cute'
    elif any(word in titulo_lower for word in ['idoso', 'senior', 'velho']):
        age_context = 'senior, mature'
    else:
        age_context = 'healthy, alert'

    if any(word in titulo_lower for word in ['cirurgia', 'surgery', 'operação']):
        setting = 'veterinary clinic, medical setting'
    elif any(word in titulo_lower for word in ['alimentação', 'food', 'nutrition', 'diet']):
        setting = 'with food bowl, feeding time'
    elif any(word in titulo_lower for word in ['exercício', 'exercise', 'atividade']):
        setting = 'outdoor, active, playing'
    elif any(word in titulo_lower for word in ['doença', 'disease', 'sick', 'saúde']):
        setting = 'veterinary examination, clinical setting'
    else:
        setting = 'clean veterinary clinic background'

    # Montar prompt final
    prompt = f"{base_context}, {age_context}, {setting}, professional photography, natural lighting, high quality, detailed, realistic"

    return prompt

def main():
    # Ler artigos
    json_path = BASE_DIR / "data" / "postagens_artigos.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        artigos = json.load(f)

    # Mapear categorias
    categorias_map = {
        1: 'dogs',
        2: 'cats',
        3: 'rodents',
        4: 'birds',
        5: 'reptiles',
        6: 'peixes'
    }

    # Gerar prompts
    prompts_output = []

    for artigo in artigos:
        id_artigo = artigo['id_postagem_artigo']
        titulo = artigo['titulo']
        id_categoria = artigo['id_categoria_artigo']
        categoria_nome = categorias_map.get(id_categoria, 'animals')

        prompt = criar_prompt_profissional(titulo, categoria_nome)

        prompts_output.append({
            'id': id_artigo,
            'titulo': titulo,
            'categoria': categoria_nome,
            'prompt': prompt,
            'filename': f'{id_artigo:08d}.jpg'
        })

    # Salvar prompts
    output_path = BASE_DIR / "data" / "prompts_artigos.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(prompts_output, f, indent=2, ensure_ascii=False)

    print(f"✓ {len(prompts_output)} prompts gerados e salvos em {output_path}")

    # Mostrar alguns exemplos
    print("\nExemplos de prompts gerados:\n")
    for item in prompts_output[:5]:
        print(f"ID {item['id']:3d} - {item['categoria']:8s}")
        print(f"  Título: {item['titulo']}")
        print(f"  Prompt: {item['prompt'][:80]}...")
        print()

if __name__ == "__main__":
    main()
