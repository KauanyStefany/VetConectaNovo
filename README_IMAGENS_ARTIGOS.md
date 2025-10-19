# Geração de Imagens dos Artigos

## Status Atual

✅ **Templates corrigidos** - Usando `/static/img/artigos/{ID:08d}.jpg`
✅ **Diretório criado** - `/static/img/artigos/`
✅ **Prompts gerados** - 100 prompts em `data/prompts_artigos.json`
⏳ **Imagens pendentes** - 100 imagens a gerar

## Custo Estimado

- Custo por imagem: $0.009
- Total de imagens: 100
- **Custo total: ~$0.90**

## Como Gerar as Imagens

### Opção 1: Geração Automática via Claude Code (Recomendado)

Peça ao Claude Code para processar em lotes:

```
"Por favor, gere as imagens dos artigos processando o arquivo
data/prompts_artigos.json usando a ferramenta mcp__runware__generate_image
em lotes de 20 artigos por vez"
```

### Opção 2: Geração Manual por Lotes

Execute o script preparado que lista todos os prompts:

```bash
python3 processar_batch_artigos.py
```

Isso mostrará os comandos necessários para cada lote.

### Opção 3: Script Automatizado

Foi criado um script `gerar_imagens_artigos_auto.py` que pode ser adaptado
para executar a geração automaticamente se você tiver acesso direto à API
do Runware.

## Arquivos Importantes

- `data/prompts_artigos.json` - Todos os prompts gerados
- `data/processar_imagens_pendentes.json` - Lista de imagens a processar
- `static/img/artigos/` - Diretório onde as imagens serão salvas

## Formato das Imagens

- Resolução: 1024x768px
- Formato: JPG
- Nome: `{ID:08d}.jpg` (ex: `00000001.jpg`)

## Fallback

Os templates já incluem fallback para as imagens de categorias caso
alguma imagem de artigo não exista:

```html
onerror="this.src='/static/img/categorias/{{ '%02d' % artigo.id_categoria_artigo }}.jpg'"
```

## Próximos Passos

1. Decidir sobre geração das imagens (custo de ~$0.90)
2. Se sim, processar em lotes de 20-25 por vez
3. Verificar imagens geradas
4. Testar a aplicação

## Visualização Atual

Mesmo sem as imagens geradas, a aplicação funciona usando as imagens
de categoria como fallback (cores corretas já aplicadas).
