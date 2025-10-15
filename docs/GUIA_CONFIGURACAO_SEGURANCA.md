# Guia Rápido de Configuração de Segurança - VetConecta

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

**Criar arquivo `.env`:**
```bash
cp .env.example .env
```

**Gerar SECRET_KEY segura:**
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))" >> .env
```

**Editar `.env` e adicionar:**
```bash
ENVIRONMENT=development
```

### 3. Iniciar a Aplicação

```bash
python main.py
```

**Ou com Uvicorn:**
```bash
uvicorn main:app --reload
```

---

## 🔐 Validação de Senha

### Requisitos de Senha (NOVO):

Todas as senhas devem ter:
- ✅ Mínimo de **8 caracteres**
- ✅ Pelo menos **1 letra maiúscula** (A-Z)
- ✅ Pelo menos **1 letra minúscula** (a-z)
- ✅ Pelo menos **1 número** (0-9)
- ✅ Pelo menos **1 caractere especial** (!@#$%^&*(),.?":{}|<>_-+=[]\\;'/)

### Senhas Rejeitadas:
- ❌ `123456`
- ❌ `password`
- ❌ `123456789`
- ❌ `12345678`
- ❌ `qwerty`
- ❌ `abc123`
- ❌ `password1`

### Exemplos de Senhas Válidas:
- ✅ `Senha@123`
- ✅ `Password1!`
- ✅ `VetConecta#2025`
- ✅ `Meu$Pet@Forte`

---

## 🔒 Rotas Protegidas

### Rotas Administrativas (requerem perfil "admin"):
- `/admin/listar_categorias`
- `/admin/alterar_categoria/{id}`
- `/admin/cadastrar_categoria`
- `/admin/excluir_categoria/{id}`
- `/admin/listar_chamados`
- `/admin/responder_chamado/{id}`
- `/admin/excluir_chamado/{id}`
- `/admin/moderar_comentarios/{id}`
- `/admin/listar_denuncias`
- `/admin/excluir_denuncia/{id}`
- `/admin/listar_verificação_crmv`
- `/admin/responder_verificação_crmv/{id}`

### Rotas de Veterinários (requerem perfil "veterinario"):
- `/veterinario/listar_postagem_artigo`
- `/veterinario/alterar_postagem_artigo/{id}`
- `/veterinario/cadastrar_postagem_artigo`
- `/veterinario/excluir_postagem_artigo/{id}`
- `/veterinario/listar_estatisticas`
- `/veterinario/obter_solicitacao_crmv`
- `/veterinario/fazer_solicitacao_crmv`

### Rotas de Tutores (requerem perfil "tutor"):
- `/tutor/listar_postagem_feed`
- `/tutor/fazer_postagem_feed`
- `/tutor/excluir_postagem_feed`

---

## 🧪 Testes de Segurança

### Teste 1: Validação de Senha
```bash
python -c "
from util.security import validar_forca_senha

# Testar senha fraca
valido, msg = validar_forca_senha('123456')
print(f'Senha 123456: {msg if not valido else \"OK\"}')

# Testar senha forte
valido, msg = validar_forca_senha('Senha@123')
print(f'Senha Senha@123: {\"OK\" if valido else msg}')
"
```

### Teste 2: Acesso Não Autorizado
```bash
# Tentar acessar rota protegida sem login
curl -i http://localhost:8000/admin/listar_categorias
# Esperado: HTTP 303 (Redirect para /login)
```

### Teste 3: Perfis de Usuário
```python
# Apenas valores válidos: "tutor" ou "veterinario"
from routes.publico.auth_routes import PerfilUsuario

print(PerfilUsuario.TUTOR)        # "tutor"
print(PerfilUsuario.VETERINARIO)  # "veterinario"
```

---

## ⚙️ Configurações de Produção

### Arquivo `.env` para Produção:

```bash
# IMPORTANTE: Use chaves diferentes em produção!
ENVIRONMENT=production
SECRET_KEY=sua_chave_producao_segura_aqui
CSRF_SECRET_KEY=sua_chave_csrf_producao_aqui
```

### Verificações Antes de Deploy:

- [ ] SECRET_KEY configurada e única
- [ ] ENVIRONMENT=production
- [ ] HTTPS configurado no servidor
- [ ] Firewall configurado
- [ ] Backups automáticos habilitados
- [ ] Logs sendo monitorados
- [ ] Rate limiting implementado (recomendado)
- [ ] CSRF implementado (recomendado)

---

## 🛡️ Segurança em Produção

### HTTPS Obrigatório
Quando `ENVIRONMENT=production`, o sistema automaticamente:
- ✅ Define `https_only=True` nos cookies de sessão
- ✅ Define `same_site="strict"` para máxima segurança
- ✅ Remove debug_link de redefinição de senha

### Sessões Seguras
- ✅ SECRET_KEY persistente (não regenera)
- ✅ Sessão regenerada a cada login (anti-fixação)
- ✅ Senha nunca armazenada na sessão
- ✅ Timeout de 1 hora

### Logging de Segurança
Eventos logados automaticamente:
- ⚠️ Tentativas de login falhadas
- ⚠️ Erros de validação
- ⚠️ Exceções de segurança
- ⚠️ Hashes inválidos

---

## 📋 Checklist de Segurança

### Antes de Cada Deploy:

#### Desenvolvimento:
- [ ] `.env` configurado com `ENVIRONMENT=development`
- [ ] SECRET_KEY gerada (pode ser temporária)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)

#### Produção:
- [ ] `.env` configurado com `ENVIRONMENT=production`
- [ ] SECRET_KEY única e segura
- [ ] CSRF_SECRET_KEY única e segura
- [ ] HTTPS habilitado no servidor
- [ ] Logs sendo salvos e monitorados
- [ ] Backups configurados
- [ ] Testes de segurança executados

---

## 🚨 Troubleshooting

### Erro: "SECRET_KEY não configurada"
```
⚠️  AVISO: SECRET_KEY não configurada. Usando chave temporária.
```

**Solução:**
1. Criar arquivo `.env`
2. Adicionar: `SECRET_KEY=sua_chave_aqui`
3. Reiniciar aplicação

### Erro: "Você não tem permissão" (403)
**Causa:** Usuário logado não tem o perfil correto para a rota

**Solução:**
- Rotas `/admin/*` requerem perfil "admin"
- Rotas `/veterinario/*` requerem perfil "veterinario"
- Rotas `/tutor/*` requerem perfil "tutor"

### Senha rejeitada no cadastro
**Causa:** Senha não atende aos requisitos de segurança

**Solução:** Criar senha com:
- Mínimo 8 caracteres
- 1 maiúscula + 1 minúscula + 1 número + 1 especial

---

## 📞 Suporte

Para dúvidas sobre segurança ou configuração, consulte:
- `docs/3_ANALISE_SEGURANCA.md` - Análise completa de segurança
- `docs/CORRECOES_SEGURANCA.md` - Detalhes das correções implementadas
- `.env.example` - Exemplo de configuração

---

**Última Atualização:** 2025-10-15
**Versão:** 1.0 com correções de segurança
