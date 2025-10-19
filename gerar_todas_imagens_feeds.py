#!/usr/bin/env python3
"""
Script para gerar imagens realistas para todas as postagens do feed
usando a API Runware através do MCP server
"""
import json
import time
import requests
from pathlib import Path

def criar_prompt_pt_para_en(descricao: str, id_postagem: int) -> str:
    """
    Traduz descrições PT-BR em prompts EN otimizados para fotos realistas de pets
    """
    # Mapeamento de contextos comuns
    prompts_especificos = {
        1: "realistic photo of a small dog doing a trick, sitting and giving paw, cute happy dog, natural lighting, pet photography",
        2: "realistic photo of a dog playing with other dogs in a park, socialization, happy dogs running, natural outdoor lighting, pet photography",
        3: "realistic photo of a dog birthday party, dog with birthday cake for dogs, celebration, happy dog, natural lighting, pet photography",
        4: "realistic photo of two cats sleeping in the sun, comfortable cats napping, warm sunlight, indoor pet photography",
        5: "realistic photo of cats using a new cat scratching post, happy cats playing, indoor natural lighting, pet photography",
        6: "realistic photo of a mischievous cat next to a knocked over flower pot, cute guilty cat, indoor scene, natural lighting",
        7: "realistic photo of a cat meowing at a water faucet, cat drinking fresh water from tap, indoor kitchen scene, natural lighting",
        8: "realistic photo of a golden retriever swimming in water, dog enjoying swimming, outdoor water scene, natural lighting, pet photography",
        9: "realistic photo of a golden retriever holding a newspaper, trained dog fetching newspaper, outdoor morning scene, natural lighting",
        10: "realistic photo of two golden retrievers playing together in a park, dog friendship, outdoor scene, natural lighting, pet photography",
        11: "realistic photo of hamsters building a nest with nesting material, cute small pets, close-up, natural lighting",
        12: "realistic photo of a hamster running on an exercise wheel, energetic hamster, pet cage setup, natural lighting",
        13: "realistic photo of hamsters exploring a maze, small pets playing, educational toy, natural lighting, close-up photography",
        14: "realistic photo of a hamster with puffy cheeks full of food, cute hamster storing food, close-up, natural lighting",
        15: "realistic photo of an alert dog barking to warn owner, protective dog indoors, home safety, natural lighting, pet photography",
        16: "realistic photo of a rescued dog, happy adopted dog portrait, emotional moment, natural lighting, pet photography",
        17: "realistic photo of a dog opening a bedroom door, smart dog using door handle, indoor scene, natural lighting",
        18: "realistic photo of rabbits eating organic carrots, cute bunnies with fresh vegetables, natural lighting, pet photography",
        19: "realistic photo of rabbits playing with a cat, interspecies friendship, cute animals together, outdoor garden, natural lighting",
        20: "realistic photo of a white rabbit sitting on owner's lap, affectionate bunny, indoor cozy scene, natural lighting",
        21: "realistic photo of a parrot saying good morning, colorful parrot close-up, natural lighting, bird photography",
        22: "realistic photo of a parrot mimicking sounds, clever bird, close-up portrait, natural lighting, bird photography",
        23: "realistic photo of a parrot singing along to guitar music, musical bird, indoor scene, natural lighting",
        24: "realistic photo of four cats sleeping together on a bed, cat pile, adorable cats cuddling, indoor scene, natural lighting",
        25: "realistic photo of a cat with a caught mouse, hunting cat, outdoor scene, natural lighting, pet photography",
        26: "realistic photo of two cats playing with a ball, energetic cats, indoor playful scene, natural lighting",
        27: "realistic photo of a cat following owner to bathroom, curious cat, indoor home scene, natural lighting",
        28: "realistic photo of a french bulldog refusing to walk, stubborn dog sitting, outdoor scene, natural lighting, pet photography",
        29: "realistic photo of a french bulldog ignoring new dog bed, funny dog sleeping on floor, indoor scene, natural lighting",
        30: "realistic photo of a snoring french bulldog, sleeping dog close-up, funny pet moment, indoor scene, natural lighting",
        31: "realistic photo of two groomed shih tzus after haircut, fluffy dogs, pet grooming result, natural lighting, pet photography",
        32: "realistic photo of shih tzu dogs playing with new toy, happy small dogs, indoor scene, natural lighting",
        33: "realistic photo of a jealous shih tzu dog, emotional dog expression, indoor scene, natural lighting, pet photography",
        34: "realistic photo of a tortoise eating lettuce, old turtle feeding, close-up, natural lighting, reptile photography",
        35: "realistic photo of a tortoise sunbathing, turtle basking in sun, outdoor summer scene, natural lighting",
        36: "realistic photo of an old tortoise birthday celebration, ancient turtle, special occasion, natural lighting, pet photography",
        37: "realistic photo of three guinea pigs in a new cage, happy cavies exploring, pet habitat, natural lighting",
        38: "realistic photo of guinea pigs eating fresh grass, cute cavies making noises, close-up, natural lighting, pet photography",
        39: "realistic photo of a pregnant guinea pig, expecting pet, gentle portrait, natural lighting, animal photography",
        40: "realistic photo of guinea pigs exploring a new playhouse, cute small pets playing, colorful habitat, natural lighting",
        41: "realistic photo of a german shepherd guarding house, protective dog alert, outdoor home security, natural lighting, pet photography",
        42: "realistic photo of a german shepherd in obedience training, smart dog learning, outdoor training scene, natural lighting",
        43: "realistic photo of a german shepherd with first place medal, winner dog, competition award, natural lighting, pet photography",
        44: "realistic photo of two betta fish with vibrant colors in aquarium, colorful fish, underwater photography, aquarium lighting",
        45: "realistic photo of a male betta fish making a bubble nest, fish behavior, aquarium close-up, natural lighting",
        46: "realistic photo of decorated aquariums with live plants, beautiful fish tanks, underwater scene, aquarium lighting",
        47: "realistic photo of a beagle chasing a squirrel in park, energetic hunting dog, outdoor action scene, natural lighting, pet photography",
        48: "realistic photo of a friendly beagle with children, social dog, outdoor neighborhood scene, natural lighting",
        49: "realistic photo of a beagle using its nose to find lost slipper, dog tracking scent, indoor scene, natural lighting",
        50: "realistic photo of five cockatiels singing together, beautiful birds chorus, morning scene, natural lighting, bird photography",
        51: "realistic photo of a cockatiel whistling a melody, talented bird, close-up portrait, natural lighting",
        52: "realistic photo of cockatiels with new toys in clean aviary, happy birds playing, colorful bird habitat, natural lighting",
        53: "realistic photo of a rottweiler protecting home from delivery person, guard dog alert, outdoor home scene, natural lighting",
        54: "realistic photo of a gentle rottweiler playing with children, family dog, safe playtime, outdoor scene, natural lighting",
        55: "realistic photo of a happy rottweiler with a large bone treat, satisfied dog, outdoor scene, natural lighting, pet photography",
        56: "realistic photo of two siamese twin cats cuddling, identical cats sleeping together, indoor cozy scene, natural lighting",
        57: "realistic photo of siamese cats meowing in harmony, vocal cats communicating, indoor scene, natural lighting, pet photography",
        58: "realistic photo of a smart siamese cat opening a cabinet door, clever cat, indoor mischief, natural lighting",
        59: "realistic photo of a pug sleeping for long hours, lazy dog napping, indoor comfortable scene, natural lighting",
        60: "realistic photo of a loudly snoring pug, funny sleeping dog, close-up, indoor scene, natural lighting",
        61: "realistic photo of a picky pug refusing food, fussy dog with food bowl, indoor scene, natural lighting, pet photography",
        62: "realistic photo of three canaries singing a symphony, beautiful songbirds, bird cage, morning light, bird photography",
        63: "realistic photo of a canary nest with eggs, bird nesting, close-up, natural lighting, bird photography",
        64: "realistic photo of canaries eating special seeds, happy songbirds feeding, bird cage, natural lighting",
        65: "realistic photo of a brave yorkshire terrier barking at large dog, small courageous dog, outdoor park scene, natural lighting",
        66: "realistic photo of a yorkshire terrier climbing onto sofa, small dog achievement, indoor scene, natural lighting",
        67: "realistic photo of a yorkshire terrier wearing a cute winter outfit, fashionable small dog, indoor scene, natural lighting",
        68: "realistic photo of ferrets escaping from their cage, mischievous pets, indoor scene, natural lighting, pet photography",
        69: "realistic photo of ferrets making a mess with toys, playful ferrets, scattered toys, indoor scene, natural lighting",
        70: "realistic photo of a ferret stealing a sock, sneaky pet behavior, indoor scene, natural lighting, funny pet moment",
        71: "realistic photo of a husky playing in snow for first time, arctic dog happy in snow, winter outdoor scene, natural lighting",
        72: "realistic photo of a husky howling at full moon, wolf-like dog, nighttime outdoor scene, moonlight",
        73: "realistic photo of a husky pulling children on a sled, sled dog in action, winter outdoor scene, natural lighting",
        74: "realistic photo of five rescued cats together, cat sanctuary, heartwarming scene, indoor natural lighting, pet photography",
        75: "realistic photo of four cats sleeping piled up on sofa, cat pile cuddle, adorable indoor scene, natural lighting",
        76: "realistic photo of healthy cats after vet checkup, happy cats at veterinary, professional pet care, natural lighting",
        77: "realistic photo of a smart poodle performing multiple tricks, trained dog showing skills, indoor scene, natural lighting",
        78: "realistic photo of a groomed poodle with fancy haircut, fluffy dog after grooming, natural lighting, pet photography",
        79: "realistic photo of an obedient poodle fetching TV remote, helpful trained dog, indoor home scene, natural lighting",
        80: "realistic photo of chinchillas taking dust bath, cute rodents bathing in sand, close-up, natural lighting, pet photography",
        81: "realistic photo of active chinchillas at night, nocturnal pets playing, evening scene, soft lighting",
        82: "realistic photo of a chinchilla jumping from high perch, acrobatic pet, cage habitat, natural lighting, action shot",
        83: "realistic photo of a border collie herding sheep efficiently, working dog in action, farm outdoor scene, natural lighting",
        84: "realistic photo of an intelligent border collie opening a gate, smart dog problem-solving, farm scene, natural lighting",
        85: "realistic photo of a border collie with gold medal at agility competition, champion dog, competition venue, natural lighting",
        86: "realistic photo of three rabbits digging tunnels in garden, bunnies creating burrows, outdoor garden scene, natural lighting",
        87: "realistic photo of a mischievous rabbit eating carrots from vegetable garden, bunny in garden, outdoor scene, natural lighting",
        88: "realistic photo of happy rabbits eating fresh planted grass, cute bunnies feeding, garden scene, natural lighting",
        89: "realistic photo of a boxer dog running 5km with owner, athletic dog jogging, outdoor exercise, natural lighting, action photography",
        90: "realistic photo of a boxer dog shadow boxing, playful dog playing with shadow, outdoor scene, natural lighting, funny pet moment",
        91: "realistic photo of a heroic boxer dog protecting home from burglar, guard dog alert, nighttime home scene, dramatic lighting",
        92: "realistic photo of two giant maine coon cats weighing 8kg each, large fluffy cats, indoor portrait, natural lighting",
        93: "realistic photo of maine coon cats being brushed, grooming large fluffy cats, indoor scene, natural lighting, pet care",
        94: "realistic photo of a maine coon cat catching a large mouse, hunter cat with prey, outdoor scene, natural lighting",
    }

    prompt = prompts_especificos.get(id_postagem, f"realistic photo, pet photography, natural lighting, {descricao}")
    return prompt + ", high quality, photorealistic"

# Baixar as primeiras 3 que já foram geradas
primeiras_urls = [
    ("00000001.jpg", "https://im.runware.ai/image/ws/2/ii/00e50072-9477-4862-8314-aed37ded0ade.jpg"),
    ("00000002.jpg", "https://im.runware.ai/image/ws/2/ii/0e2af369-6c8b-42e2-8b20-5c376d162bf5.jpg"),
    ("00000003.jpg", "https://im.runware.ai/image/ws/2/ii/9f708895-aba2-486b-9875-cbd128ad94e7.jpg"),
]

output_dir = Path('static/img/feeds')
output_dir.mkdir(parents=True, exist_ok=True)

print("Baixando primeiras 3 imagens já geradas...")
for filename, url in primeiras_urls:
    filepath = output_dir / filename
    if not filepath.exists():
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✓ Salvo: {filename}")
        else:
            print(f"✗ Erro ao baixar: {filename}")
    else:
        print(f"⊘ Já existe: {filename}")

print("\nPrimeiras 3 imagens salvas com sucesso!")
print("Execute o script principal para gerar as demais 91 imagens.")
