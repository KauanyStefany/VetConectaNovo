# Como Gerar as 100 Imagens dos Artigos

## Status Atual

TODO o código está pronto! Os templates já usam as imagens corretas e têm fallback.

## Para Gerar as 100 Imagens

Como são 100 imagens ($0.90 de custo total), existem duas formas:

### Opção 1: Solicitar Geração Automática

Peça ao Claude Code em uma NOVA conversa:

```
"Por favor, processe o arquivo data/prompts_artigos.json e gere todas
as imagens usando mcp__runware__generate_image, salvando em 
static/img/artigos/ com os nomes especificados no JSON"
```

### Opção 2: Gerar Manualmente em Lotes

Execute este comando e cole em uma conversa com Claude Code:

```bash
python3 processar_batch_artigos.py
```

Isso mostrará todos os prompts organizados em lotes de 10.

## Arquivos Prontos

✅ `data/prompts_artigos.json` - 100 prompts contextualizados
✅ `templates/componentes/artigos_recentes.html` - Usando imagens corretas
✅ `templates/publico/artigos.html` - Usando imagens corretas
✅ `static/img/artigos/` - Diretório criado

## Sistema Funcionando AGORA

Mesmo sem gerar as imagens, o site JÁ FUNCIONA:
- Cores das categorias aplicadas ✅
- Fallback para imagens de categoria ✅
- Layout responsivo ✅

Teste em: http://127.0.0.1:8000/
