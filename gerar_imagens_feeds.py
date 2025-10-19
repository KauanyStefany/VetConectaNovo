import json
import time
import requests
from pathlib import Path

# Carregar postagens
with open('data/postagens_feeds.json', 'r', encoding='utf-8') as f:
    postagens = json.load(f)

# Diretório de saída
output_dir = Path('static/img/feeds')
output_dir.mkdir(parents=True, exist_ok=True)

# Função para traduzir descrição em prompt realista
def criar_prompt(descricao: str) -> str:
    """
    Cria um prompt em inglês para gerar foto realista baseada na descrição
    """
    # Palavras-chave para criar contexto fotográfico realista
    prompt = f"realistic photo, high quality, natural lighting, pet photography, {descricao}"
    return prompt

# Processar cada postagem
total = len(postagens)
print(f"Gerando {total} imagens...")

for i, postagem in enumerate(postagens, 1):
    id_postagem = postagem['id_postagem_feed']
    descricao = postagem['descricao']

    # Nome do arquivo: ID com 8 dígitos + .jpg
    filename = f"{id_postagem:08d}.jpg"
    filepath = output_dir / filename

    # Pular se já existe
    if filepath.exists():
        print(f"[{i}/{total}] Pulando {filename} (já existe)")
        continue

    print(f"[{i}/{total}] Gerando {filename}...")
    print(f"  Descrição: {descricao[:80]}...")

    # Criar prompt
    prompt = criar_prompt(descricao)
    print(f"  Prompt: {prompt[:80]}...")

    # Aqui você precisará integrar com a API de geração de imagens
    # Por enquanto, vou criar um placeholder para mostrar a estrutura

    # Aguardar um pouco entre requisições para não sobrecarregar
    time.sleep(1)

print("Concluído!")
