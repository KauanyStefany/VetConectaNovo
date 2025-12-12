# ✅ ENTREGAS PARA AGW - VERSÃO OTIMIZADA.

https://pagespeed.web.dev/ - justificando a parte de otimização de imagens: joguem a url do site de vocês aqui, e vejam essas dicas sobre imagens.
**exemplo:** 

![image.png](attachment:32bfbaf1-f83b-448e-9c0b-8ac9a3d56b5b:image.png)

## 🎨 DESIGN SYSTEM & CORES

- [x]  2 famílias tipográficas (use a que vocês definiram no overleaf).
    
    **1 para títulos** (Páginas e seções (qualquer texto cuja função seja organizar, hierarquizar e guiar o olhar do usuário)
    
    **1 para textos** (textos corridos, descrição, funcionais.)) 
    
    **Caso não queira usar com a importação do google fonts, faça o download da família tipográfica e use-a.**
    
- [x]  Escala de cores a partir da paleta definida anteriormente por vocês, com variações (claro/escuro) da cor principal e secundaria (para apoiar a principal sem tirar o foco dela).
A **escala de cores** é a **série de variações** de uma única cor da paleta, indo do tom mais claro ao mais escuro. Adote a abordagem em que se há aumento de saturação o brilho diminui, se há aumento de brilho a saturação diminui (HSB). Você consegue essas variações no [coolors.co](http://coolors.co), acessando a opção view shaders do que fica disponível ao passar o cursor do mouse em cima da cor escolhida.
    
    **Exemplo:** Se quisesse um tom mais escuro de vermelho da sua paleta primaria, para substituir o tom preto dos títulos, você poderia usar o site [coolors.co](http://coolors.co/) acessar a opção view shaders que fica disponível ao passar o cursor do mouse em cima da cor escolhida, e escolher o tom mais escuro do vermelho. Então, uma de suas variações seria esta apontada pela seta branca (#120202).
    
    ![image.png](attachment:a0b1345f-26fd-49c3-9736-c066920aec03:image.png)
    
- [x]  Conceito "cor sobre cor" (uma mesma cor, com pelo menos 2 variações) aplicado (em ao menos 1 componente (card, botão, section, form, etc)). Atendendo a este item, você atende ao item Escala de cores definido acima…
    
    **Exemplo:** 
    
    ![Aqui tem variações a partir de um único tom de verde.](attachment:625f2f8b-2d0f-4c0a-a700-1644b41377e0:image.png)
    
    Aqui tem variações a partir de um único tom de verde.
    
- [x]  Fazer o uso de variáveis css para padronizar (família tipográfica, cores, espaçamento(opcional)). Faça o uso em ao menos um local.
    
    Exemplo de definição das variáveis:
    
    ```css
    :root {
    	/* ---------------------------------- */
    	/* 1. CORES (Baseado em Escala HSL/Tailwind) */
    	/* ---------------------------------- */
    	
    	/* CORES PRIMÁRIAS (Ex: Azul Principal) */
    	--ds-color-primary-50: #e0f2ff;   /* Fundo muito suave */
    	--ds-color-primary-500: #007bff; /* Cor pura / Botões principais */
    	--ds-color-primary-700: #0056b3; /* Hover / Destaque */
    	--ds-color-primary-900: #003c7d; /* Texto ou Dark Mode */
    
    	/* CORES NEUTRAS (Fundo, Borda, Texto) */
    	--ds-color-white: #ffffff;      /* Branco puro */
    	--ds-color-black: #111111;      /* Preto suave */
    	--ds-color-gray-100: #f8f9fa;  /* Fundo da seção */
    	--ds-color-gray-700: #495057;  /* Texto secundário */
    	
    	/* CORES DE FEEDBACK (Sem escala para simplificar) */
    	--ds-color-success: #28a745;
    	--ds-color-error: #dc3545;
    	
    	/* ---------------------------------- */
    	/* 2. TIPOGRAFIA */
    	/* ---------------------------------- */
    	
    	/* FONT FAMILY */
    	--ds-font-family-titulo: 'Montserrat', sans-serif; /* Expressiva, para h1-h6 */
    	--ds-font-family-texto: 'Roboto', sans-serif;    /* Legível, para P, Labels, Botões */
    
    	/* TAMANHOS DE TEXTO (Opcional, mas útil para Body/Padrão) */
    	--ds-font-size-base: 1rem;       /* 16px */
    	--ds-line-height-base: 1.5;
    
    	/* ---------------------------------- */
    	/* 3. ESPAÇAMENTO (Base Modular 8px) */
    	/* ---------------------------------- */
    	
    	--ds-spacing-xs: 4px;   /* Extra Small */
    	--ds-spacing-sm: 8px;   /* Small / Base */
    	--ds-spacing-md: 16px;  /* Medium / 2x Base */
    	--ds-spacing-lg: 24px;  /* Large / 3x Base */
    	--ds-spacing-xl: 32px;  /* Extra Large / 4x Base */
    }
    ```
    

exemplo de uso:

```css
.titulo{
	font-family:--var(--ds-font-family-titulo);
}
```

## 🖼️ ELEMENTOS GRÁFICOS & SVG

- [x]  Logo em SVG (vetorizada). Use o https://convertio.co/ ou outros que conheça, como SVG é um código, é possível usar a propriedade fill, e trocar a cor. Use webp somente for uma logo complexa com muitas cores, ao menos o tamanho da imagem em bytes será reduzido.

Exemplo:

![image.png](attachment:b007f9b5-fc4b-4790-a819-8fbad38bf446:image.png)

- [ ]  Imagens otimizadas (WebP ~~+ fallback~~). O ideal é que todo projeto atenda a esses requisitos, porém para esta atividade, ao menos uma página ***onde você usa imagens estáticas(aquelas independente de cadastro)*** deve ter essas otimizações.
    
    Neste caso, se tiver alguma imagem em jpg, faça o uso da estratégia de ~~fallback, e~~ tenha ~~e use~~ também a mesma imagem em webP. ~~em duas dimensões original do seu projeto e outra com 2x o tamanho da original, dando prioridade para que a mesma (em webP) seja renderizada primeiro.~~
    
    veja detalhes em: [Otimização e tratamento de imagens para WEB.](https://www.notion.so/Otimiza-o-e-tratamento-de-imagens-para-WEB-2a9c9ec8232e80fa8808f6a292cc1e82?pvs=21)
    

## 💻 IMPLEMENTAÇÃO RESPONSIVA

- [x]  Grid system (Sistema de grids do bootstrap).
- [x]  Layout mobile-first.
- [x]  Navegação responsiva.

## ⚡ INTERATIVIDADE & ESTADOS

- [x]  Estados hover/focus/active. Valido se houver ao menos em uma página elementos que o usuário interage ao passar o cursor do mouse mude a cor ou suspenda, o importante é ter alguma modificação do estado, que indique ao usuário que aquele elemento é interativo(vai acontecer alguma coisa ao clicar).
- [x]  Animações CSS em elementos interativos. Ao atender o item de cima, este item é atendido
- [x]  Formulários com validação visual. Ex: Formularios que informam ao usuário a força da senha, ou como ele deve fazer a senha, ou que indique que ele fez algo certo, ou errado.
- [x]  Feedback visual para ações. Atendido se o item acima for atendido.

## 🎯 ACESSIBILIDADE & PERFORMANCE

- [x]  Contraste de cores adequado. Ex: textos com cores contrastantes do background, que permitam a leitura com facilidade.
- [ ]  Lazy loading para imagens. data-attributes loading=”lazy” nas tags img

[Cores.](https://www.notion.so/Cores-2b0c9ec8232e8010b32ef3d79041ce22?pvs=21)