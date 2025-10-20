# Gerador de Imagens para Artigos do VetConecta

Este documento explica como usar o script `gerar_imagens_artigos.py` para gerar imagens fotorrealistas para os artigos do VetConecta.

## Visão Geral

O script gera automaticamente imagens 1024x768 em formato JPG de alta qualidade para os 48 novos artigos (IDs 101-148) usando IA generativa (Runware AI).

## Arquivos Criados

- **gerar_imagens_artigos.py** - Script principal de geração
- **data/prompts_imagens_artigos.json** - Arquivo com todos os prompts gerados (referência)

## Como Usar

### 1. Executar o Script

```bash
python gerar_imagens_artigos.py
```

### 2. Quando a API Runware Estiver Disponível

Atualmente, a API Runware está temporariamente indisponível. Quando voltar a funcionar:

#### Opção A: Usar MCP (Model Context Protocol) - Recomendado

O VetConecta já possui integração MCP com Runware. Basta executar o script que ele tentará usar a ferramenta MCP disponível.

#### Opção B: Integração Direta com API

Descomente as linhas indicadas no script e instale a biblioteca:

```bash
pip install runware
```

### 3. Alternativa: Gerar Manualmente

Se preferir gerar as imagens em outro serviço (DALL-E, Midjourney, Stable Diffusion), use o arquivo `data/prompts_imagens_artigos.json` como referência.

Cada entrada contém:
- `id_artigo`: ID do artigo
- `titulo`: Título do artigo
- `categoria_id`: Categoria (3=Pequenos Mamíferos, 4=Aves, 5=Répteis, 6=Peixes)
- `prompt`: Prompt otimizado em inglês
- `output_file`: Nome do arquivo de saída (ex: `00000101.jpg`)

## Estrutura de Diretórios

```
VetConectaNovo/
├── data/
│   ├── postagens_artigos.json          # Artigos originais
│   └── prompts_imagens_artigos.json    # Prompts gerados
├── static/
│   └── img/
│       └── artigos/                     # Diretório de saída das imagens
│           ├── 00000101.jpg
│           ├── 00000102.jpg
│           └── ...
└── gerar_imagens_artigos.py            # Script de geração
```

## Especificações das Imagens

- **Formato**: JPG
- **Dimensões**: 1024x768 pixels
- **Qualidade**: Alta (40 steps de inferência)
- **Estilo**: Fotorrealista, contexto veterinário profissional
- **Nomenclatura**: `{ID:08d}.jpg` (ex: `00000101.jpg`)

## Categorias e Contextos

O script gera prompts específicos baseados na categoria:

| Categoria ID | Tipo | Contexto |
|--------------|------|----------|
| 3 | Pequenos Mamíferos | Hamsters, coelhos, porquinhos-da-índia, chinchilas |
| 4 | Aves | Calopsitas, papagaios, canários, periquitos |
| 5 | Répteis | Iguanas, serpentes, pogonas, tartarugas |
| 6 | Peixes | Aquários, bettas, guppys, peixes ornamentais |

## Exemplos de Prompts Gerados

### Artigo 101 - Alimentação adequada para calopsitas
```
Photorealistic veterinary image related to bird avian veterinary care,
professional medical setting, high quality detailed photography,
natural lighting, 8k quality, focused on alimentação adequada para calopsitas
```

### Artigo 117 - Bettas: cuidados específicos
```
Photorealistic veterinary image related to fish aquarium aquatic care,
professional medical setting, high quality detailed photography,
natural lighting, 8k quality, focused on bettas: cuidados específicos
```

## Personalização

Para personalizar prompts específicos, edite o dicionário `prompts_especificos` no arquivo `gerar_imagens_artigos.py` (linhas 58-140).

## Verificação de Progresso

O script automaticamente:
- Verifica se imagens já existem (não sobrescreve)
- Mostra progresso em tempo real
- Gera relatório final com estatísticas
- Salva todos os prompts em JSON para referência

## Solução de Problemas

### API Runware indisponível

**Erro**: `Server Error. Please try again later.`

**Solução**:
1. Aguardar alguns minutos e tentar novamente
2. Verificar se há problemas conhecidos no serviço Runware
3. Usar alternativa manual com os prompts do arquivo JSON

### Diretório de saída não existe

**Erro**: `No such file or directory: 'static/img/artigos'`

**Solução**: O script cria automaticamente, mas você pode criar manualmente:
```bash
mkdir -p static/img/artigos
```

### Artigos não encontrados

**Erro**: `Arquivo data/postagens_artigos.json não encontrado!`

**Solução**: Execute o script a partir do diretório raiz do projeto:
```bash
cd /Volumes/Externo/Ifes/VetConectaNovo
python gerar_imagens_artigos.py
```

## Artigos Contemplados

O script gera imagens para os seguintes 48 artigos:

### Aves (IDs 101-112)
- Alimentação de calopsitas
- Doenças respiratórias
- Enriquecimento para papagaios
- Problemas de bico e unhas
- Reprodução de canários
- Psitacose
- Manejo sanitário
- Anestesia em aves
- Terapias naturais
- Transporte seguro
- Prevenção de intoxicações
- Muda de penas

### Peixes (IDs 113-124)
- Qualidade da água
- Doenças em peixes ornamentais
- Alimentação de peixes tropicais
- Montagem de aquário marinho
- Cuidados com bettas
- Compatibilidade entre espécies
- Reprodução de guppys
- Filtragem eficiente
- Iluminação para plantados
- Aquários de quarentena
- Peixes limpa-vidros
- Controle de algas

### Pequenos Mamíferos (IDs 125-136)
- Alimentação de hamsters
- Habitação para coelhos
- Doenças dentárias
- Cuidados com porquinhos-da-índia
- Comportamento de chinchilas
- Reprodução de hamsters
- Enriquecimento para ratos
- Sinais de doença em coelhos
- Castração
- Estresse térmico
- Escolha de substrato
- Parasitas

### Répteis (IDs 137-148)
- Temperatura para iguanas
- Alimentação de serpentes
- Terrário para pogona
- Iluminação UVB
- Doença metabólica óssea
- Hidratação de répteis
- Ecdise (troca de pele)
- Infecções respiratórias
- Quarentena de répteis
- Suplementação nutricional
- Reprodução de leopard geckos
- Manejo de tartarugas aquáticas

## Manutenção

Para adicionar novos artigos no futuro:

1. Adicione os artigos em `data/postagens_artigos.json`
2. Atualize o range `ARTIGOS_NOVOS_IDS` no script
3. (Opcional) Adicione prompts específicos em `prompts_especificos`
4. Execute o script novamente

## Suporte

Para problemas ou dúvidas:
- Verifique este README
- Consulte os logs de execução do script
- Revise o arquivo `data/prompts_imagens_artigos.json`

---

**Criado em**: 2025-10-20
**Última atualização**: 2025-10-20
**Versão do Script**: 1.0
