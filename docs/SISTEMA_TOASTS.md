# Sistema de Mensagens com Toasts - VetConecta

Sistema completo de notificações toast integrado com FastAPI e Bootstrap 5.3.

## Visão Geral

O sistema de toasts do VetConecta permite exibir mensagens de feedback ao usuário de forma elegante e não intrusiva. As mensagens podem ser:

- **Mensagens Flash** - Persistem através de redirects usando sessões
- **Mensagens JavaScript** - Exibidas diretamente via JavaScript

## Componentes do Sistema

### 1. Backend - Python

#### Arquivo: `util/mensagens.py`

Funções para gerenciar mensagens flash no backend:

```python
from fastapi import Request
from util.mensagens import (
    adicionar_mensagem_sucesso,
    adicionar_mensagem_erro,
    adicionar_mensagem_aviso,
    adicionar_mensagem_info,
    obter_mensagens
)

# Adicionar mensagens
adicionar_mensagem_sucesso(request, "Operação realizada com sucesso!")
adicionar_mensagem_erro(request, "Erro ao processar requisição")
adicionar_mensagem_aviso(request, "Atenção: dados não salvos")
adicionar_mensagem_info(request, "Informação importante")

# Obter mensagens (usado nos templates)
mensagens = obter_mensagens(request)
```

**Funções disponíveis:**

| Função | Descrição | Tipo |
|--------|-----------|------|
| `adicionar_mensagem(request, mensagem, tipo)` | Função genérica | `success`, `danger`, `warning`, `info` |
| `adicionar_mensagem_sucesso(request, mensagem)` | Mensagem de sucesso | `success` |
| `adicionar_mensagem_erro(request, mensagem)` | Mensagem de erro | `danger` |
| `adicionar_mensagem_aviso(request, mensagem)` | Mensagem de aviso | `warning` |
| `adicionar_mensagem_info(request, mensagem)` | Mensagem informativa | `info` |
| `obter_mensagens(request)` | Recupera e limpa mensagens | Lista de dicts |

**Aliases para compatibilidade:**
- `flash()` → `adicionar_mensagem()`
- `informar_sucesso()` → `adicionar_mensagem_sucesso()`
- `informar_erro()` → `adicionar_mensagem_erro()`
- `informar_aviso()` → `adicionar_mensagem_aviso()`
- `informar_info()` → `adicionar_mensagem_info()`
- `get_flashed_messages()` → `obter_mensagens()`

### 2. Frontend - JavaScript

#### Arquivo: `static/js/toasts.js`

Gerenciador de toasts usando Bootstrap 5.3:

```javascript
// Funções globais disponíveis
showSuccess("Operação concluída!");
showError("Erro ao processar!");
showWarning("Atenção!");
showInfo("Informação importante");

// Função genérica com duração customizada
showToast("Mensagem", "success", 10000); // 10 segundos

// Toast permanente (não desaparece automaticamente)
showToast("Importante!", "warning", 0);

// Usando o manager diretamente
window.toastManager.show("Olá", "info", 5000);
```

**Funções disponíveis:**

| Função | Descrição | Duração Padrão |
|--------|-----------|----------------|
| `showSuccess(mensagem, duracao)` | Toast de sucesso | 5000ms (5s) |
| `showError(mensagem, duracao)` | Toast de erro | 7000ms (7s) |
| `showWarning(mensagem, duracao)` | Toast de aviso | 6000ms (6s) |
| `showInfo(mensagem, duracao)` | Toast informativo | 5000ms (5s) |
| `showToast(mensagem, tipo, duracao)` | Toast genérico | 5000ms (5s) |

**Parâmetros:**
- `mensagem` (string): Texto a exibir
- `tipo` (string): `success`, `danger`, `warning`, `info`
- `duracao` (number): Milissegundos (0 = permanente)

### 3. Estilos - CSS

#### Arquivo: `static/css/base.css`

Estilos customizados com as cores do VetConecta:

```css
/* Toast Customization */
.toast-container {
    z-index: 9999;
}

.toast {
    min-width: 250px;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

/* Cores personalizadas para toasts */
.toast.text-bg-success {
    background-color: var(--cor-verde) !important;
}

.toast.text-bg-warning {
    background-color: var(--cor-laranja) !important;
}

.toast.text-bg-danger {
    background-color: var(--cor-rosa) !important;
}
```

**Cores:**
- Sucesso: Verde (`#2D5D5C`)
- Aviso: Laranja (`#FA811D`)
- Erro: Rosa (`#CA567C`)
- Info: Azul padrão Bootstrap

### 4. Templates - HTML

#### Template Base: `templates/base_publica.html`

O template base já inclui:

```html
<!-- Container para Toasts -->
<div id="toast-container" class="toast-container position-fixed bottom-0 end-0 p-3 toast-offset"></div>

<!-- Dados de mensagens (hidden) -->
<script id="mensagens-data" type="application/json">
    {{ obter_mensagens(request) | tojson }}
</script>

<!-- Bootstrap 5.3.8 JavaScript Bundle -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>

<!-- Script de Toasts -->
<script src="/static/js/toasts.js"></script>
```

## Uso Completo

### Exemplo 1: Mensagem Flash em Rota

```python
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro

router = APIRouter()

@router.post("/cadastro")
async def cadastrar(request: Request):
    try:
        # ... lógica de cadastro ...
        adicionar_mensagem_sucesso(request, "Cadastro realizado com sucesso!")
        return RedirectResponse(url="/login", status_code=302)
    except Exception as e:
        adicionar_mensagem_erro(request, f"Erro ao cadastrar: {str(e)}")
        return RedirectResponse(url="/cadastro", status_code=302)
```

### Exemplo 2: Mensagem Direta em JavaScript

```html
{% extends "base_publica.html" %}

{% block conteudo %}
<button onclick="salvarDados()">Salvar</button>
{% endblock %}

{% block scripts %}
<script>
async function salvarDados() {
    try {
        const response = await fetch('/api/salvar', { method: 'POST' });
        if (response.ok) {
            showSuccess("Dados salvos com sucesso!");
        } else {
            showError("Erro ao salvar dados");
        }
    } catch (error) {
        showError("Erro na requisição");
    }
}
</script>
{% endblock %}
```

### Exemplo 3: Múltiplas Mensagens

```python
from util.mensagens import (
    adicionar_mensagem_sucesso,
    adicionar_mensagem_aviso
)

@router.post("/processar")
async def processar(request: Request):
    adicionar_mensagem_sucesso(request, "Arquivo processado")
    adicionar_mensagem_aviso(request, "Algumas linhas foram ignoradas")
    return RedirectResponse(url="/resultado", status_code=302)
```

### Exemplo 4: Toast Permanente

```javascript
// Toast que não desaparece automaticamente
showToast("Leia esta mensagem importante!", "warning", 0);

// Usuário precisa clicar no X para fechar
```

### Exemplo 5: Toast com Duração Customizada

```javascript
// Toast de 15 segundos
showSuccess("Upload concluído! Processando...", 15000);

// Toast de 3 segundos (rápido)
showInfo("Clique novamente para confirmar", 3000);
```

## Tipos de Toast

### Success (Sucesso)
- **Cor:** Verde (`--cor-verde`)
- **Ícone:** `bi-check-circle-fill`
- **Duração:** 5 segundos
- **Uso:** Operações bem-sucedidas, confirmações

### Danger (Erro)
- **Cor:** Rosa (`--cor-rosa`)
- **Ícone:** `bi-x-circle-fill`
- **Duração:** 7 segundos
- **Uso:** Erros, falhas, validações

### Warning (Aviso)
- **Cor:** Laranja (`--cor-laranja`)
- **Ícone:** `bi-exclamation-triangle-fill`
- **Duração:** 6 segundos
- **Uso:** Avisos, alertas não críticos

### Info (Informação)
- **Cor:** Azul Bootstrap
- **Ícone:** `bi-info-circle-fill`
- **Duração:** 5 segundos
- **Uso:** Informações gerais, dicas

## Fluxo de Funcionamento

### Mensagens Flash (Backend → Frontend)

```
1. Usuário submete formulário
   ↓
2. Backend processa requisição
   ↓
3. Backend chama adicionar_mensagem_sucesso(request, "...")
   ↓
4. Mensagem armazenada em request.session["_mensagens"]
   ↓
5. Backend retorna RedirectResponse
   ↓
6. Nova página é carregada
   ↓
7. Template renderiza <script id="mensagens-data">
   ↓
8. toasts.js lê mensagens e chama showToast()
   ↓
9. Toast é exibido ao usuário
   ↓
10. Toast desaparece após duração ou clique em X
```

### Mensagens JavaScript Diretas

```
1. Evento JavaScript (click, submit, etc.)
   ↓
2. Código chama showSuccess("...") diretamente
   ↓
3. ToastManager cria elemento HTML do toast
   ↓
4. Toast é inserido no #toast-container
   ↓
5. Bootstrap.Toast é inicializado
   ↓
6. Toast é exibido com animação
   ↓
7. Toast desaparece após duração ou clique em X
```

## Personalização

### Alterar Duração Padrão

Edite `static/js/toasts.js`:

```javascript
// Métodos de conveniência
success(message, duration = 8000) { // era 5000
    return this.show(message, 'success', duration);
}
```

### Adicionar Novo Tipo

1. **CSS** (`static/css/base.css`):
```css
.toast.text-bg-primary {
    background-color: var(--cor-roxo) !important;
}
```

2. **JavaScript** (`static/js/toasts.js`):
```javascript
const typeClasses = {
    'success': 'text-bg-success',
    'danger': 'text-bg-danger',
    'warning': 'text-bg-warning',
    'info': 'text-bg-info',
    'primary': 'text-bg-primary'  // Novo tipo
};

const typeIcons = {
    // ...
    'primary': 'bi-star-fill'  // Novo ícone
};

// Adicionar método de conveniência
primary(message, duration = 5000) {
    return this.show(message, 'primary', duration);
}

// Adicionar função global
window.showPrimary = function(message, duration = 5000) {
    return window.toastManager.primary(message, duration);
};
```

3. **Python** (`util/mensagens.py`):
```python
def adicionar_mensagem_primary(request: Request, mensagem: str) -> None:
    """Adiciona mensagem primary"""
    adicionar_mensagem(request, mensagem, "primary")
```

### Alterar Posição dos Toasts

Edite `templates/base_publica.html`:

```html
<!-- Bottom-Right (padrão) -->
<div id="toast-container" class="toast-container position-fixed bottom-0 end-0 p-3"></div>

<!-- Top-Right -->
<div id="toast-container" class="toast-container position-fixed top-0 end-0 p-3"></div>

<!-- Top-Center -->
<div id="toast-container" class="toast-container position-fixed top-0 start-50 translate-middle-x p-3"></div>

<!-- Bottom-Center -->
<div id="toast-container" class="toast-container position-fixed bottom-0 start-50 translate-middle-x p-3"></div>
```

## Segurança

### Proteção contra XSS

O sistema inclui escape de HTML automático:

```javascript
escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;  // Automaticamente escapa HTML
    return div.innerHTML;
}
```

**Mensagens seguras:**
```javascript
showSuccess("<script>alert('xss')</script>");
// Exibe literalmente: <script>alert('xss')</script>
// NÃO executa o script
```

### Validação de Tipos

As funções validam os tipos de mensagem:

```javascript
const typeClasses = {
    'success': 'text-bg-success',
    'danger': 'text-bg-danger',
    'warning': 'text-bg-warning',
    'info': 'text-bg-info'
};

const bgClass = typeClasses[type] || 'text-bg-info';  // Fallback seguro
```

## Boas Práticas

### 1. Escolha o Tipo Correto

```python
# ✓ BOM - Tipo adequado
adicionar_mensagem_sucesso(request, "Login realizado")

# ✗ RUIM - Tipo inadequado
adicionar_mensagem_info(request, "Erro crítico!")  # Deveria ser erro
```

### 2. Mensagens Claras e Concisas

```python
# ✓ BOM - Mensagem clara
adicionar_mensagem_sucesso(request, "Artigo publicado com sucesso")

# ✗ RUIM - Mensagem vaga
adicionar_mensagem_info(request, "OK")
```

### 3. Use Mensagens Flash para Redirects

```python
# ✓ BOM - Mensagem persiste através do redirect
adicionar_mensagem_sucesso(request, "Dados salvos")
return RedirectResponse(url="/dashboard", status_code=302)

# ✗ RUIM - Mensagem não aparecerá após redirect
return templates.TemplateResponse("dashboard.html", {
    "request": request,
    "mensagem": "Dados salvos"  # Perdida no redirect
})
```

### 4. Use JavaScript para Feedback Imediato

```javascript
// ✓ BOM - Feedback imediato sem recarregar página
async function curtir(postId) {
    await fetch(`/api/curtir/${postId}`, { method: 'POST' });
    showSuccess("Curtido!");
}

// ✗ RUIM - Recarrega página desnecessariamente
// (usar apenas quando redirect for necessário)
```

### 5. Evite Múltiplas Mensagens Simultâneas

```python
# ✓ BOM - Uma mensagem consolidada
adicionar_mensagem_sucesso(request,
    "Cadastro concluído. E-mail de confirmação enviado.")

# ✗ RUIM - Muitas mensagens ao mesmo tempo
adicionar_mensagem_sucesso(request, "Cadastro concluído")
adicionar_mensagem_info(request, "E-mail enviado")
adicionar_mensagem_aviso(request, "Confirme seu e-mail")
```

## Troubleshooting

### Mensagens não aparecem

**Problema:** Toasts não são exibidos

**Soluções:**
1. Verifique se `toasts.js` está carregado:
   ```html
   <script src="/static/js/toasts.js"></script>
   ```

2. Verifique se Bootstrap está carregado ANTES de `toasts.js`:
   ```html
   <script src=".../bootstrap.bundle.min.js"></script>
   <script src="/static/js/toasts.js"></script>
   ```

3. Verifique se o container existe:
   ```html
   <div id="toast-container" ...></div>
   ```

4. Abra o console do navegador para ver erros

### Mensagens Flash não persistem

**Problema:** Mensagens desaparecem após redirect

**Solução:** Certifique-se de que `SessionMiddleware` está configurado:

```python
# util/middlewares.py
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(
    SessionMiddleware,
    secret_key="sua-chave-secreta"
)
```

### Estilos não aplicados

**Problema:** Toasts aparecem sem cores/estilos

**Solução:** Verifique se `base.css` está carregado:
```html
<link href="/static/css/base.css" rel="stylesheet">
```

### Toast não desaparece

**Problema:** Toast fica na tela indefinidamente

**Solução:** Verifique se Bootstrap está inicializado corretamente:

```javascript
// Deve estar presente em toasts.js
const bsToast = new bootstrap.Toast(toast, {
    autohide: duration > 0,  // true se duration > 0
    delay: duration
});
```

## Arquivo de Configuração

### Estrutura de Arquivos

```
VetConectaNovo/
├── static/
│   ├── css/
│   │   └── base.css          # Estilos dos toasts
│   └── js/
│       └── toasts.js         # Gerenciador de toasts
├── templates/
│   └── base_publica.html     # Template base com container
├── util/
│   ├── mensagens.py          # Backend flash messages
│   └── template_util.py      # Helper templates
└── docs/
    └── SISTEMA_TOASTS.md     # Esta documentação
```

## Changelog

### v1.0.0 (2025-01-XX)
- ✨ Implementação inicial do sistema de toasts
- 🎨 Integração com cores do VetConecta
- 🔒 Proteção contra XSS
- 📝 Documentação completa
- ✅ 4 tipos de mensagem (success, danger, warning, info)
- 🔄 Suporte a mensagens flash via sessão
- ⚡ Suporte a mensagens JavaScript diretas

## Suporte

Para dúvidas ou problemas:
1. Consulte esta documentação
2. Verifique exemplos nos arquivos de rotas existentes
3. Veja o código fonte em `static/js/toasts.js`
4. Consulte a documentação do Bootstrap Toast: https://getbootstrap.com/docs/5.3/components/toasts/

---

**VetConecta** - Sistema de Mensagens Toast v1.0.0
