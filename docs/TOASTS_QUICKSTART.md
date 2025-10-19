# Sistema de Toasts - Guia Rápido

## Instalação Concluída ✓

O sistema de toasts já está implementado e pronto para uso!

## Uso Rápido

### Backend (Python)

```python
from util.mensagens import (
    adicionar_mensagem_sucesso,
    adicionar_mensagem_erro,
    adicionar_mensagem_aviso,
    adicionar_mensagem_info
)

# Em suas rotas:
@router.post("/salvar")
async def salvar(request: Request):
    adicionar_mensagem_sucesso(request, "Dados salvos!")
    return RedirectResponse(url="/dashboard", status_code=302)
```

### Frontend (JavaScript)

```javascript
// Mensagens diretas sem recarregar a página
showSuccess("Operação concluída!");
showError("Erro ao processar!");
showWarning("Atenção!");
showInfo("Informação importante");

// Com duração customizada (em milissegundos)
showToast("Mensagem", "success", 10000); // 10 segundos
```

## Tipos Disponíveis

| Função | Tipo | Cor | Ícone |
|--------|------|-----|-------|
| `showSuccess()` / `adicionar_mensagem_sucesso()` | success | Verde | ✓ |
| `showError()` / `adicionar_mensagem_erro()` | danger | Rosa | ✕ |
| `showWarning()` / `adicionar_mensagem_aviso()` | warning | Laranja | ⚠ |
| `showInfo()` / `adicionar_mensagem_info()` | info | Azul | ℹ |

## Demonstração

Acesse a página de demonstração para ver o sistema em ação:

**URL:** `http://localhost:8000/demo-toasts/`

Para habilitar a rota de demonstração, adicione em `main.py`:

```python
from routes.publico import toast_demo_routes

app.include_router(toast_demo_routes.router)
```

## Arquivos Criados

```
✓ static/js/toasts.js              - Gerenciador JavaScript
✓ util/mensagens.py                - API Python para mensagens flash
✓ static/css/base.css              - Estilos customizados (atualizado)
✓ templates/base_publica.html      - Template base (atualizado)
✓ util/template_util.py            - Helper templates (atualizado)
✓ routes/publico/toast_demo_routes.py - Página de demonstração
✓ templates/publico/demo_toasts.html  - Template de demonstração
✓ docs/SISTEMA_TOASTS.md          - Documentação completa
```

## Documentação Completa

Para informações detalhadas, exemplos avançados e troubleshooting:

📚 **[docs/SISTEMA_TOASTS.md](./SISTEMA_TOASTS.md)**

---

**VetConecta** - Sistema de Toasts v1.0.0
